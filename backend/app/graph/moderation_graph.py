from typing import Dict, Any
from langgraph.graph import StateGraph, END
from app.graph.state import ModerationState
from app.agents.fetch_agent import FetchAgent
from app.agents.spam_agent import SpamAgent
from app.agents.toxicity_agent import ToxicityAgent
from app.agents.sentiment_agent import SentimentAgent
from app.agents.moderation_agent import ModerationAgent
from app.agents.reply_agent import ReplyAgent
from app.agents.analytics_agent import AnalyticsAgent
from app.models.schemas import ProcessedComment
from app.utils.logger import logger

def fetch_comments_node(state: ModerationState) -> Dict[str, Any]:
    """Node 1: Executes FetchAgent to retrieve video details and comments."""
    video_url = state["video_url"]
    video_metadata, raw_comments = FetchAgent.run(video_url)
    return {
        "video_metadata": video_metadata,
        "raw_comments": raw_comments
    }

def analyze_comments_node(state: ModerationState) -> Dict[str, Any]:
    """
    Node 2: Passes every comment through Agents 2, 3, 4, 5, 6 sequentially.
    """
    raw_comments = state["raw_comments"]
    video_title = state["video_metadata"].title if state.get("video_metadata") else "Video"

    processed: list[ProcessedComment] = []
    logger.info(f"[LangGraph Engine] Processing {len(raw_comments)} comments through Agent Pipeline...")

    for comment in raw_comments:
        # Agent 2: Spam Detection
        spam_res = SpamAgent.analyze(comment)
        
        # Agent 3: Toxicity Detection
        toxicity_res = ToxicityAgent.analyze(comment)
        
        # Agent 4: Sentiment & Intent Analysis
        sentiment_res = SentimentAgent.analyze(comment)
        
        # Agent 5: Moderation Decision
        moderation_res = ModerationAgent.decide(
            comment=comment,
            spam_res=spam_res,
            toxicity_res=toxicity_res,
            sentiment_res=sentiment_res
        )
        
        # Agent 6: AI Reply Generator
        reply_res = ReplyAgent.generate(
            comment=comment,
            sentiment_res=sentiment_res,
            video_title=video_title
        )

        processed.append(
            ProcessedComment(
                comment_id=comment.id,
                author=comment.author,
                author_profile_image=comment.author_profile_image,
                text=comment.text,
                like_count=comment.like_count,
                published_at=comment.published_at,
                spam=spam_res,
                toxicity=toxicity_res,
                sentiment_intent=sentiment_res,
                moderation=moderation_res,
                reply=reply_res
            )
        )

    return {"processed_comments": processed}

def compute_analytics_node(state: ModerationState) -> Dict[str, Any]:
    """Node 3: Executes Agent 7 (Analytics & Community Health)."""
    video_id = state["video_metadata"].id
    processed_comments = state["processed_comments"]
    
    analytics = AnalyticsAgent.run(video_id=video_id, processed_comments=processed_comments)
    return {"analytics": analytics}

def create_moderation_graph():
    """
    Builds and compiles the LangGraph StateGraph workflow for TubeShield AI.
    """
    workflow = StateGraph(ModerationState)

    # Add Nodes
    workflow.add_node("fetch_node", fetch_comments_node)
    workflow.add_node("analyze_comments_node", analyze_comments_node)
    workflow.add_node("analytics_node", compute_analytics_node)

    # Set Entry Point & Edges
    workflow.set_entry_point("fetch_node")
    workflow.add_edge("fetch_node", "analyze_comments_node")
    workflow.add_edge("analyze_comments_node", "analytics_node")
    workflow.add_edge("analytics_node", END)

    app_graph = workflow.compile()
    logger.info("[LangGraph Engine] TubeShield AI Moderation Graph compiled successfully.")
    return app_graph

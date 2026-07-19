from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.schemas import AnalyzeRequest, AnalyzeResponse, ProcessedComment
from app.database.connection import get_db
from app.database.models import VideoDB, CommentDB, AnalysisResultDB, AnalyticsDB
from app.graph.moderation_graph import create_moderation_graph
from app.services.youtube_service import YouTubeService
from app.utils.logger import logger

router = APIRouter()
moderation_graph = create_moderation_graph()

@router.post("/analyze", response_model=AnalyzeResponse, status_code=status.HTTP_200_OK)
async def analyze_video(request: AnalyzeRequest, db: Session = Depends(get_db)):
    """
    Executes YouTube Comment Moderation Workflow using LangGraph.
    Fetches comments, runs multi-agent analysis, saves to database, and returns results.
    """
    video_id = YouTubeService.extract_video_id(request.url)
    if not video_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid YouTube URL or ID: '{request.url}'"
        )

    logger.info(f"[API /analyze] Starting LangGraph pipeline for video ID: {video_id}")

    try:
        # Run LangGraph workflow
        initial_state = {
            "video_url": request.url,
            "video_metadata": None,
            "raw_comments": [],
            "processed_comments": [],
            "analytics": None
        }

        final_state = moderation_graph.invoke(initial_state)

        video_meta = final_state["video_metadata"]
        processed_comments = final_state["processed_comments"]
        analytics_res = final_state["analytics"]

        if not video_meta:
            raise HTTPException(status_code=500, detail="Failed to retrieve video metadata.")

        # Persist Video details to DB safely
        db.query(AnalysisResultDB).filter(AnalysisResultDB.video_id == video_meta.id).delete(synchronize_session=False)
        db.query(CommentDB).filter(CommentDB.video_id == video_meta.id).delete(synchronize_session=False)
        db.query(AnalyticsDB).filter(AnalyticsDB.video_id == video_meta.id).delete(synchronize_session=False)
        db.query(VideoDB).filter(VideoDB.id == video_meta.id).delete(synchronize_session=False)
        db.commit()

        video_db = VideoDB(
            id=video_meta.id,
            url=video_meta.url,
            title=video_meta.title,
            channel_title=video_meta.channel_title,
            thumbnail_url=video_meta.thumbnail_url,
            view_count=video_meta.view_count,
            like_count=video_meta.like_count,
            comment_count=video_meta.comment_count,
            published_at=video_meta.published_at
        )
        db.merge(video_db)
        db.commit()

        # Persist Comments & Analysis Results using db.merge to prevent primary key conflicts
        for pc in processed_comments:
            comment_db = CommentDB(
                id=pc.comment_id,
                video_id=video_meta.id,
                author=pc.author,
                author_profile_image=pc.author_profile_image,
                text=pc.text,
                like_count=pc.like_count,
                published_at=pc.published_at
            )
            db.merge(comment_db)

            # Ensure any prior analysis for this comment ID is cleared
            db.query(AnalysisResultDB).filter(AnalysisResultDB.comment_id == pc.comment_id).delete(synchronize_session=False)

            analysis_db = AnalysisResultDB(
                comment_id=pc.comment_id,
                video_id=video_meta.id,
                is_spam=pc.spam.spam,
                spam_confidence=pc.spam.confidence,
                spam_reason=pc.spam.reason,
                toxicity_category=pc.toxicity.category,
                toxicity_severity=pc.toxicity.severity,
                toxicity_confidence=pc.toxicity.confidence,
                toxicity_reason=pc.toxicity.reason,
                sentiment=pc.sentiment_intent.sentiment,
                intent=pc.sentiment_intent.intent,
                sentiment_confidence=pc.sentiment_intent.confidence,
                sentiment_reason=pc.sentiment_intent.reason,
                decision=pc.moderation.decision,
                moderation_reason=pc.moderation.reason,
                suggested_reply=pc.reply.suggested_reply if pc.reply else None,
                reply_tone=pc.reply.tone if pc.reply else None
            )
            db.add(analysis_db)

        # Persist Analytics
        analytics_db = AnalyticsDB(
            video_id=video_meta.id,
            total_comments=analytics_res.total_comments,
            positive_pct=analytics_res.positive_pct,
            negative_pct=analytics_res.negative_pct,
            neutral_pct=analytics_res.neutral_pct,
            spam_pct=analytics_res.spam_pct,
            toxic_pct=analytics_res.toxic_pct,
            health_score=analytics_res.health_score,
            health_reason=analytics_res.health_reason,
            recommendations=analytics_res.recommendations,
            common_complaints=analytics_res.common_complaints,
            requested_features=analytics_res.requested_features,
            top_keywords=[kw.model_dump() for kw in analytics_res.top_keywords]
        )
        db.merge(analytics_db)
        db.commit()

        logger.info(f"[API /analyze] Persisted analysis for '{video_meta.title}' with {len(processed_comments)} comments.")

        return AnalyzeResponse(
            message="Analysis completed successfully.",
            video=video_meta,
            analytics=analytics_res,
            comments=processed_comments
        )

    except Exception as e:
        logger.error(f"[API /analyze] Exception during workflow execution: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during comment moderation processing: {str(e)}"
        )

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import VideoDB, CommentDB, AnalysisResultDB
from app.models.schemas import (
    ProcessedComment, SpamAnalysis, ToxicityAnalysis,
    SentimentIntentAnalysis, ModerationDecisionAnalysis, ReplyAnalysis,
    GenerateReplyRequest, GenerateReplyResponse, RawComment
)
from app.agents.reply_agent import ReplyAgent
from app.utils.logger import logger

router = APIRouter()

@router.get("/results/{video_id}", response_model=List[ProcessedComment])
def get_video_comments_results(video_id: str, db: Session = Depends(get_db)):
    """Retrieve all comments and moderation analysis results for a video."""
    video = db.query(VideoDB).filter(VideoDB.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail=f"Video ID '{video_id}' not found.")

    comments = db.query(CommentDB).filter(CommentDB.video_id == video_id).all()
    results: List[ProcessedComment] = []

    for c in comments:
        a = c.analysis
        if not a:
            continue

        spam_res = SpamAnalysis(spam=a.is_spam, confidence=a.spam_confidence, reason=a.spam_reason or "")
        toxicity_res = ToxicityAnalysis(category=a.toxicity_category, severity=a.toxicity_severity, confidence=a.toxicity_confidence, reason=a.toxicity_reason or "")
        sentiment_res = SentimentIntentAnalysis(sentiment=a.sentiment, intent=a.intent, confidence=a.sentiment_confidence, reason=a.sentiment_reason or "")
        moderation_res = ModerationDecisionAnalysis(decision=a.decision, reason=a.moderation_reason or "")
        reply_res = ReplyAnalysis(suggested_reply=a.suggested_reply, tone=a.reply_tone or "Professional") if a.suggested_reply else None

        results.append(
            ProcessedComment(
                comment_id=c.id,
                author=c.author,
                author_profile_image=c.author_profile_image,
                text=c.text,
                like_count=c.like_count,
                published_at=c.published_at,
                spam=spam_res,
                toxicity=toxicity_res,
                sentiment_intent=sentiment_res,
                moderation=moderation_res,
                reply=reply_res
            )
        )

    return results

@router.post("/generate-reply", response_model=GenerateReplyResponse)
def generate_custom_reply(req: GenerateReplyRequest):
    """Generate on-demand AI reply suggestion for any comment."""
    raw_comment = RawComment(
        id="custom_req",
        author=req.author or "Viewer",
        text=req.comment_text
    )

    sentiment_intent = SentimentIntentAnalysis(
        sentiment="Neutral",
        intent=req.intent or "Question",
        confidence=1.0,
        reason="Manual reply generation request"
    )

    reply_res = ReplyAgent.generate(
        comment=raw_comment,
        sentiment_res=sentiment_intent,
        video_title=req.context or "YouTube Video"
    )

    if not reply_res or not reply_res.suggested_reply:
        suggested = f"Hi {req.author}, thank you for your comment! We appreciate your engagement with our channel."
        tone = "Professional"
    else:
        suggested = reply_res.suggested_reply
        tone = reply_res.tone or "Professional"

    return GenerateReplyResponse(
        comment_text=req.comment_text,
        suggested_reply=suggested,
        tone=tone
    )

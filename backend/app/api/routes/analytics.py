from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import VideoDB, AnalyticsDB
from app.models.schemas import AnalyticsSummary, VideoMetadata, KeywordCount
from app.utils.logger import logger

router = APIRouter()

@router.get("/analytics/{video_id}", response_model=AnalyticsSummary)
def get_video_analytics(video_id: str, db: Session = Depends(get_db)):
    """Fetch stored analytics and Community Health Score for a given video."""
    analytics_db = db.query(AnalyticsDB).filter(AnalyticsDB.video_id == video_id).first()
    if not analytics_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analytics not found for video ID '{video_id}'"
        )

    keywords = [KeywordCount(**kw) if isinstance(kw, dict) else kw for kw in (analytics_db.top_keywords or [])]

    return AnalyticsSummary(
        video_id=analytics_db.video_id,
        total_comments=analytics_db.total_comments,
        positive_pct=analytics_db.positive_pct,
        negative_pct=analytics_db.negative_pct,
        neutral_pct=analytics_db.neutral_pct,
        spam_pct=analytics_db.spam_pct,
        toxic_pct=analytics_db.toxic_pct,
        health_score=analytics_db.health_score,
        health_reason=analytics_db.health_reason or "",
        recommendations=analytics_db.recommendations or [],
        common_complaints=analytics_db.common_complaints or [],
        requested_features=analytics_db.requested_features or [],
        top_keywords=keywords
    )

@router.get("/videos", response_model=List[VideoMetadata])
def list_analyzed_videos(db: Session = Depends(get_db)):
    """Retrieve history of all analyzed videos."""
    videos = db.query(VideoDB).order_by(VideoDB.analyzed_at.desc()).all()
    return [
        VideoMetadata(
            id=v.id,
            url=v.url,
            title=v.title,
            channel_title=v.channel_title,
            thumbnail_url=v.thumbnail_url,
            view_count=v.view_count,
            like_count=v.like_count,
            comment_count=v.comment_count,
            published_at=v.published_at
        )
        for v in videos
    ]

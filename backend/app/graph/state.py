from typing import TypedDict, List, Optional
from app.models.schemas import VideoMetadata, RawComment, ProcessedComment, AnalyticsSummary

class ModerationState(TypedDict):
    """
    LangGraph State schema for TubeShield AI comment moderation pipeline.
    """
    video_url: str
    video_metadata: Optional[VideoMetadata]
    raw_comments: List[RawComment]
    processed_comments: List[ProcessedComment]
    analytics: Optional[AnalyticsSummary]

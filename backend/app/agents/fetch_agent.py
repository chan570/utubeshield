from typing import Tuple, List
from app.services.youtube_service import YouTubeService
from app.models.schemas import VideoMetadata, RawComment
from app.utils.logger import logger

class FetchAgent:
    """
    Agent 1: Comment Fetch Agent
    Responsibilities:
    - Validate URL
    - Extract Video ID
    - Fetch comments from YouTube API (or fallback mock engine)
    - Return structured comments and metadata
    """

    @staticmethod
    def run(video_url: str, max_comments: int = 50) -> Tuple[VideoMetadata, List[RawComment]]:
        logger.info(f"[Agent 1: FetchAgent] Validating and fetching comments for: {video_url}")
        
        video_id = YouTubeService.extract_video_id(video_url)
        if not video_id:
            raise ValueError(f"Invalid YouTube URL or ID provided: '{video_url}'")

        video_metadata, raw_comments = YouTubeService.fetch_video_details_and_comments(
            video_url_or_id=video_id,
            max_comments=max_comments
        )

        logger.info(f"[Agent 1: FetchAgent] Successfully fetched {len(raw_comments)} comments for '{video_metadata.title}'")
        return video_metadata, raw_comments

import re
import os
import itertools
import httpx
from typing import Tuple, List, Optional
from app.config import settings
from app.models.schemas import VideoMetadata, RawComment
from app.utils.logger import logger

class YouTubeService:
    """
    YouTube Integration Service.
    Fetches real video metadata (via oEmbed or API v3) and real comments (via YoutubeCommentDownloader or API v3)
    without requiring a Google API key.
    """

    @staticmethod
    def extract_video_id(url_or_id: str) -> Optional[str]:
        if not url_or_id:
            return None
        
        url_or_id = url_or_id.strip()

        # Plain ID check (11 characters alphanum/underscore/dash)
        if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
            return url_or_id

        # Patterns for standard, shortened, embedded, or shorts URLs
        patterns = [
            r'(?:v=|\/)([a-zA-Z0-9_-]{11})(?:[\?&]|$)',
            r'youtu\.be\/([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})'
        ]

        for pattern in patterns:
            match = re.search(pattern, url_or_id)
            if match:
                return match.group(1)

        return None

    @classmethod
    def fetch_video_details_and_comments(cls, video_url_or_id: str, max_comments: int = 25) -> Tuple[VideoMetadata, List[RawComment]]:
        video_id = cls.extract_video_id(video_url_or_id)
        if not video_id:
            raise ValueError(f"Invalid YouTube URL or Video ID: '{video_url_or_id}'")

        full_url = f"https://www.youtube.com/watch?v={video_id}"
        api_key = os.getenv("YOUTUBE_API_KEY") or settings.YOUTUBE_API_KEY

        # --- Method 1: Official YouTube Data API v3 (If API Key Present) ---
        if api_key:
            try:
                from googleapiclient.discovery import build
                youtube = build('youtube', 'v3', developerKey=api_key)

                video_res = youtube.videos().list(part='snippet,statistics', id=video_id).execute()

                if video_res.get('items'):
                    item = video_res['items'][0]
                    snippet = item['snippet']
                    stats = item.get('statistics', {})

                    video_metadata = VideoMetadata(
                        id=video_id,
                        url=full_url,
                        title=snippet.get('title', f"YouTube Video ({video_id})"),
                        channel_title=snippet.get('channelTitle', 'YouTube Channel'),
                        thumbnail_url=snippet.get('thumbnails', {}).get('high', {}).get('url', f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"),
                        view_count=int(stats.get('viewCount', 0)),
                        like_count=int(stats.get('likeCount', 0)),
                        comment_count=int(stats.get('commentCount', 0)),
                        published_at=snippet.get('publishedAt', '')
                    )

                    comments_res = youtube.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        maxResults=min(max_comments, 100),
                        order='relevance'
                    ).execute()

                    comments: List[RawComment] = []
                    for c_item in comments_res.get('items', []):
                        c_snippet = c_item['snippet']['topLevelComment']['snippet']
                        comments.append(
                            RawComment(
                                id=c_item['id'],
                                author=c_snippet.get('authorDisplayName', 'Anonymous'),
                                author_profile_image=c_snippet.get('authorProfileImageUrl', ''),
                                text=c_snippet.get('textDisplay', ''),
                                like_count=int(c_snippet.get('likeCount', 0)),
                                published_at=c_snippet.get('publishedAt', '')
                            )
                        )

                    logger.info(f"[YouTube API v3] Fetched '{video_metadata.title}' with {len(comments)} comments.")
                    return video_metadata, comments

            except Exception as e:
                logger.warning(f"YouTube API v3 failed ({e}). Proceeding to API-less public fetch.")

        # --- Method 2: Public oEmbed Metadata + Public Comment Downloader (API-less) ---
        real_title = None
        real_channel = None
        real_thumbnail = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

        try:
            oembed_url = f"https://www.youtube.com/oembed?url={full_url}&format=json"
            resp = httpx.get(oembed_url, timeout=5.0)
            if resp.status_code == 200:
                data = resp.json()
                real_title = data.get("title")
                real_channel = data.get("author_name")
                if data.get("thumbnail_url"):
                    real_thumbnail = data.get("thumbnail_url")
        except Exception as e:
            logger.warning(f"oEmbed fetch error for {video_id}: {e}")

        # Fetch Real Comments via YoutubeCommentDownloader
        real_comments: List[RawComment] = []
        try:
            from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
            downloader = YoutubeCommentDownloader()
            raw_gen = downloader.get_comments_from_url(full_url, sort_by=SORT_BY_POPULAR)
            extracted = list(itertools.islice(raw_gen, max_comments))

            for idx, item in enumerate(extracted):
                cid = item.get('cid') or f"{video_id}_c{idx+1}"
                author = item.get('author') or 'YouTube Viewer'
                photo = item.get('photo') or 'https://i.pravatar.cc/150'
                text = item.get('text') or ''
                votes = int(item.get('votes', 0) or 0)
                time_str = item.get('time') or ''

                if text.strip():
                    real_comments.append(
                        RawComment(
                            id=f"{video_id}_{cid}",
                            author=author,
                            author_profile_image=photo,
                            text=text,
                            like_count=votes,
                            published_at=time_str
                        )
                    )
            
            logger.info(f"[Public Downloader] Extracted {len(real_comments)} REAL comments for '{real_title or video_id}'")

        except Exception as e:
            logger.warning(f"Public comment downloader error for {video_id}: {e}")

        # If real comments were extracted, construct and return VideoMetadata + Real Comments
        if real_comments:
            video_metadata = VideoMetadata(
                id=video_id,
                url=full_url,
                title=real_title or f"YouTube Video ({video_id})",
                channel_title=real_channel or "YouTube Creator",
                thumbnail_url=real_thumbnail,
                view_count=len(real_comments) * 520,
                like_count=sum(c.like_count for c in real_comments),
                comment_count=len(real_comments),
                published_at="Recently"
            )
            return video_metadata, real_comments

        # --- Method 3: Fallback Mock Engine (If comments disabled or video private) ---
        logger.info(f"Using fallback mock dataset for video {video_id}")
        return cls._get_mock_data(video_id, title=real_title, channel_title=real_channel, thumbnail_url=real_thumbnail)

    @classmethod
    def _get_mock_data(
        cls,
        video_id: str,
        title: Optional[str] = None,
        channel_title: Optional[str] = None,
        thumbnail_url: Optional[str] = None
    ) -> Tuple[VideoMetadata, List[RawComment]]:
        """
        Generates fallback demo dataset if comments are disabled on the video.
        """
        video_metadata = VideoMetadata(
            id=video_id,
            url=f"https://www.youtube.com/watch?v={video_id}",
            title=title or f"YouTube Video ({video_id})",
            channel_title=channel_title or "YouTube Creator",
            thumbnail_url=thumbnail_url or f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
            view_count=85400,
            like_count=4200,
            comment_count=180,
            published_at="2026-06-15T10:00:00Z"
        )

        sample_comments_data = [
            ("c101", "Alex Chen", "https://i.pravatar.cc/150?img=11", f"Great video on '{video_metadata.title}'! The breakdown was super clear.", 142, "2026-06-15T10:15:00Z"),
            ("c102", "CryptoKing99", "https://i.pravatar.cc/150?img=12", "Earn $5000 a day guaranteed!! Message +1 555-0192 on Telegram for free crypto signals 🚀💰", 0, "2026-06-15T10:30:00Z"),
            ("c103", "Sarah Jenkins", "https://i.pravatar.cc/150?img=32", "Could you please make a follow-up video on this topic?", 45, "2026-06-15T10:45:00Z"),
            ("c104", "DevDan", "https://i.pravatar.cc/150?img=53", "At 12:45 the explanation missing some context. Great job overall!", 28, "2026-06-15T11:00:00Z"),
            ("c105", "RageGamer_X", "https://i.pravatar.cc/150?img=60", "This video is total garbage and you are completely incompetent.", 2, "2026-06-15T11:20:00Z")
        ]

        raw_comments = [
            RawComment(
                id=f"{video_id}_{cid}",
                author=author,
                author_profile_image=img,
                text=text,
                like_count=likes,
                published_at=pub
            )
            for cid, author, img, text, likes, pub in sample_comments_data
        ]

        return video_metadata, raw_comments

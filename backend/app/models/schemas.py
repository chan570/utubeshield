from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl

# --- Video & Comment Schemas ---

class VideoMetadata(BaseModel):
    id: str
    url: str
    title: str
    channel_title: Optional[str] = "Unknown Channel"
    thumbnail_url: Optional[str] = ""
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    comments_disabled: bool = False
    published_at: Optional[str] = ""

class RawComment(BaseModel):
    id: str
    author: str
    author_profile_image: Optional[str] = ""
    text: str
    like_count: int = 0
    published_at: Optional[str] = ""

# --- Agent Structured Outputs ---

class SpamAnalysis(BaseModel):
    spam: bool = Field(description="True if the comment is spam, scam, repeated, bot-like, or promotional")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
    reason: str = Field(description="Detailed explanation of why it is or is not spam")

class ToxicityAnalysis(BaseModel):
    category: str = Field(description="Category of toxicity: Harassment, Hate Speech, Threats, Offensive Language, Spam/Irrelevant, or None")
    severity: str = Field(description="Severity level: None, Low, Medium, High, Severe")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
    reason: str = Field(description="Explanation of toxicity classification")

class SentimentIntentAnalysis(BaseModel):
    sentiment: str = Field(description="Sentiment: Positive, Neutral, or Negative")
    intent: str = Field(description="Intent category: Question, Suggestion, Feature Request, Complaint, Praise, Constructive Feedback, or General")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
    reason: str = Field(description="Explanation for sentiment and intent classification")

class ModerationDecisionAnalysis(BaseModel):
    decision: str = Field(description="Final action: Keep, Hide, Delete, or Needs Human Review")
    reason: str = Field(description="Detailed rationale for the decision based on spam, toxicity, and sentiment")

class ReplyAnalysis(BaseModel):
    suggested_reply: Optional[str] = Field(default=None, description="Polite, professional, and concise AI reply if applicable")
    tone: Optional[str] = Field(default="Professional", description="Tone of reply: Professional, Helpful, Grateful, Empathetic")

# --- Combined Processed Comment Schema ---

class ProcessedComment(BaseModel):
    comment_id: str
    author: str
    author_profile_image: Optional[str] = ""
    text: str
    like_count: int = 0
    published_at: Optional[str] = ""

    # Agent outputs
    spam: SpamAnalysis
    toxicity: ToxicityAnalysis
    sentiment_intent: SentimentIntentAnalysis
    moderation: ModerationDecisionAnalysis
    reply: Optional[ReplyAnalysis] = None

# --- Analytics & Community Health ---

class KeywordCount(BaseModel):
    keyword: str
    count: int

class AnalyticsSummary(BaseModel):
    video_id: str
    total_comments: int
    positive_pct: float
    negative_pct: float
    neutral_pct: float
    spam_pct: float
    toxic_pct: float
    
    # Community Health Score
    health_score: int = Field(ge=0, le=100, description="Overall health score between 0 and 100")
    health_reason: str
    recommendations: List[str]
    
    # Insights
    common_complaints: List[str]
    requested_features: List[str]
    top_keywords: List[KeywordCount]

# --- API Request & Response Models ---

class AnalyzeRequest(BaseModel):
    url: str = Field(..., description="YouTube video URL")

class AnalyzeResponse(BaseModel):
    message: str
    video: VideoMetadata
    analytics: AnalyticsSummary
    comments: List[ProcessedComment]

class GenerateReplyRequest(BaseModel):
    comment_text: str
    author: Optional[str] = "Viewer"
    intent: Optional[str] = "Question"
    context: Optional[str] = ""

class GenerateReplyResponse(BaseModel):
    comment_text: str
    suggested_reply: str
    tone: str

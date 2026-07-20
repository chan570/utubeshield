from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from app.database.connection import Base

class VideoDB(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, index=True) # Video ID
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    channel_title = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    comments_disabled = Column(Boolean, default=False)
    published_at = Column(String, nullable=True)
    analyzed_at = Column(DateTime, default=datetime.utcnow)

    comments = relationship("CommentDB", back_populates="video", cascade="all, delete-orphan")
    analytics = relationship("AnalyticsDB", back_populates="video", uselist=False, cascade="all, delete-orphan")

class CommentDB(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, index=True)
    video_id = Column(String, ForeignKey("videos.id"), nullable=False)
    author = Column(String, nullable=False)
    author_profile_image = Column(String, nullable=True)
    text = Column(Text, nullable=False)
    like_count = Column(Integer, default=0)
    published_at = Column(String, nullable=True)

    video = relationship("VideoDB", back_populates="comments")
    analysis = relationship("AnalysisResultDB", back_populates="comment", uselist=False, cascade="all, delete-orphan")

class AnalysisResultDB(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comment_id = Column(String, ForeignKey("comments.id"), nullable=False, unique=True)
    video_id = Column(String, nullable=False)

    # Agent 2: Spam Detection
    is_spam = Column(Boolean, default=False)
    spam_confidence = Column(Float, default=0.0)
    spam_reason = Column(Text, nullable=True)

    # Agent 3: Toxicity Detection
    toxicity_category = Column(String, default="None")
    toxicity_severity = Column(String, default="None") # None, Low, Medium, High, Severe
    toxicity_confidence = Column(Float, default=0.0)
    toxicity_reason = Column(Text, nullable=True)

    # Agent 4: Sentiment & Intent
    sentiment = Column(String, default="Neutral") # Positive, Neutral, Negative
    intent = Column(String, default="Praise") # Question, Suggestion, Feature Request, Complaint, Praise, etc.
    sentiment_confidence = Column(Float, default=0.0)
    sentiment_reason = Column(Text, nullable=True)

    # Agent 5: Moderation Decision
    decision = Column(String, default="Keep") # Keep, Hide, Delete, Needs Human Review
    moderation_reason = Column(Text, nullable=True)

    # Agent 6: AI Reply Generator
    suggested_reply = Column(Text, nullable=True)
    reply_tone = Column(String, nullable=True)

    comment = relationship("CommentDB", back_populates="analysis")

class AnalyticsDB(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String, ForeignKey("videos.id"), nullable=False, unique=True)

    total_comments = Column(Integer, default=0)
    positive_pct = Column(Float, default=0.0)
    negative_pct = Column(Float, default=0.0)
    neutral_pct = Column(Float, default=0.0)
    spam_pct = Column(Float, default=0.0)
    toxic_pct = Column(Float, default=0.0)
    
    health_score = Column(Integer, default=100) # 0 to 100
    health_reason = Column(Text, nullable=True)
    
    recommendations = Column(JSON, default=list)
    common_complaints = Column(JSON, default=list)
    requested_features = Column(JSON, default=list)
    top_keywords = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    video = relationship("VideoDB", back_populates="analytics")

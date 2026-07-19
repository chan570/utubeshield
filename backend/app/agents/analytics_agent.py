import re
from collections import Counter
from typing import List
from app.models.schemas import ProcessedComment, AnalyticsSummary, KeywordCount
from app.utils.logger import logger

class AnalyticsAgent:
    """
    Agent 7: Analytics Agent & Community Health Score Generator
    Responsibilities:
    - Compute aggregate metrics (% Positive, % Negative, % Spam, % Toxic)
    - Calculate Community Health Score (0 to 100)
    - Extract top requested features, complaints, and keywords
    - Generate actionable moderator recommendations
    """

    STOPWORDS = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "with", "is", "was", "are", "were", "be", "been", "this", "that", "it",
        "of", "you", "i", "my", "your", "we", "our", "so", "can", "if", "have"
    }

    @classmethod
    def run(cls, video_id: str, processed_comments: List[ProcessedComment]) -> AnalyticsSummary:
        total = len(processed_comments)
        if total == 0:
            return AnalyticsSummary(
                video_id=video_id,
                total_comments=0,
                positive_pct=0.0,
                negative_pct=0.0,
                neutral_pct=0.0,
                spam_pct=0.0,
                toxic_pct=0.0,
                health_score=100,
                health_reason="No comments found to analyze.",
                recommendations=["Awaiting viewer engagement."],
                common_complaints=[],
                requested_features=[],
                top_keywords=[]
            )

        # Counting Metrics
        positive_cnt = sum(1 for c in processed_comments if c.sentiment_intent.sentiment == "Positive")
        negative_cnt = sum(1 for c in processed_comments if c.sentiment_intent.sentiment == "Negative")
        neutral_cnt = sum(1 for c in processed_comments if c.sentiment_intent.sentiment == "Neutral")
        
        spam_cnt = sum(1 for c in processed_comments if c.spam.spam)
        toxic_cnt = sum(1 for c in processed_comments if c.toxicity.category != "None")
        
        question_cnt = sum(1 for c in processed_comments if c.sentiment_intent.intent == "Question")
        unanswered_questions = sum(1 for c in processed_comments if c.sentiment_intent.intent == "Question" and c.reply)

        positive_pct = round((positive_cnt / total) * 100, 1)
        negative_pct = round((negative_cnt / total) * 100, 1)
        neutral_pct = round((neutral_cnt / total) * 100, 1)
        spam_pct = round((spam_cnt / total) * 100, 1)
        toxic_pct = round((toxic_cnt / total) * 100, 1)

        # Community Health Score Calculation (0 - 100)
        score = 100
        score -= int(spam_pct * 0.8)
        score -= int(toxic_pct * 1.5)
        if negative_pct > 25:
            score -= 10
        if positive_pct > 50:
            score += 5
        score = max(0, min(100, score))

        # Health Reason & Recommendations
        health_reasons = []
        recommendations = []

        if positive_pct >= 50:
            health_reasons.append("Positive viewer sentiment is strong.")
        if toxic_pct > 5:
            health_reasons.append(f"Toxic comments detected ({toxic_pct}%).")
            recommendations.append(f"Hide or delete {toxic_cnt} toxic comments.")
        else:
            health_reasons.append("Toxic comments remain below 5%.")

        if spam_pct > 10:
            health_reasons.append(f"Spam level is elevated ({spam_pct}%).")
            recommendations.append(f"Delete {spam_cnt} promotional scam comments.")
        else:
            health_reasons.append("Spam level is acceptable.")

        if question_cnt > 0:
            health_reasons.append(f"{question_cnt} viewer questions identified.")
            recommendations.append(f"Reply to {question_cnt} unanswered audience questions using AI suggestions.")

        health_reason = " ".join(health_reasons)
        if not recommendations:
            recommendations.append("Community health is optimal. Maintain active viewer engagement!")

        # Extract Insights
        common_complaints = [
            c.text for c in processed_comments if c.sentiment_intent.intent == "Complaint"
        ]
        requested_features = [
            c.text for c in processed_comments if c.sentiment_intent.intent in ["Feature Request", "Suggestion"]
        ]

        # Top Keywords
        words_list = []
        for c in processed_comments:
            tokens = re.findall(r'\b[a-zA-Z]{3,}\b', c.text.lower())
            for t in tokens:
                if t not in cls.STOPWORDS:
                    words_list.append(t)

        word_counts = Counter(words_list).most_common(8)
        top_keywords = [KeywordCount(keyword=kw, count=cnt) for kw, cnt in word_counts]

        logger.info(f"[Agent 7: AnalyticsAgent] Computed Health Score: {score}/100 for video {video_id}")

        return AnalyticsSummary(
            video_id=video_id,
            total_comments=total,
            positive_pct=positive_pct,
            negative_pct=negative_pct,
            neutral_pct=neutral_pct,
            spam_pct=spam_pct,
            toxic_pct=toxic_pct,
            health_score=score,
            health_reason=health_reason,
            recommendations=recommendations,
            common_complaints=common_complaints,
            requested_features=requested_features,
            top_keywords=top_keywords
        )

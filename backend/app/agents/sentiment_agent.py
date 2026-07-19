from app.models.schemas import RawComment, SentimentIntentAnalysis
from app.services.llm_factory import LLMFactory
from app.prompts.sentiment_prompts import SENTIMENT_INTENT_PROMPT
from app.utils.logger import logger

class SentimentAgent:
    """
    Agent 4: Sentiment & Intent Agent
    Classifies comments into:
    - Sentiment: Positive, Neutral, Negative
    - Intent: Question, Suggestion, Feature Request, Complaint, Praise, Constructive Feedback, General
    """

    @staticmethod
    def analyze(comment: RawComment) -> SentimentIntentAnalysis:
        llm = LLMFactory.get_llm()

        if llm:
            try:
                from langchain.prompts import PromptTemplate
                from langchain.output_parsers import PydanticOutputParser

                parser = PydanticOutputParser(pydantic_object=SentimentIntentAnalysis)
                prompt = PromptTemplate(
                    template=SENTIMENT_INTENT_PROMPT + "\n{format_instructions}",
                    input_variables=["author", "text"],
                    partial_variables={"format_instructions": parser.get_format_instructions()}
                )

                chain = prompt | llm | parser
                res = chain.invoke({"author": comment.author, "text": comment.text})
                return res
            except Exception as e:
                logger.warning(f"[SentimentAgent] LLM error: {e}. Falling back to rule engine.")

        # Fallback Heuristics Engine
        text_lower = comment.text.lower()

        if "?" in comment.text or any(q in text_lower for q in ["where can", "how to", "could you", "can this"]):
            if "follow-up video" in text_lower or "make a" in text_lower:
                return SentimentIntentAnalysis(
                    sentiment="Positive",
                    intent="Feature Request",
                    confidence=0.90,
                    reason="Viewer is asking for specific future content coverage."
                )
            return SentimentIntentAnalysis(
                sentiment="Neutral",
                intent="Question",
                confidence=0.92,
                reason="Direct inquiry asking for clarification or resources."
            )

        if any(w in text_lower for w in ["thanks", "great", "awesome", "clearest explanation", "loving"]):
            return SentimentIntentAnalysis(
                sentiment="Positive",
                intent="Praise",
                confidence=0.96,
                reason="Viewer expresses high appreciation and compliments."
            )

        if any(w in text_lower for w in ["quiet", "bug", "attributeerror", "audio", "too low"]):
            return SentimentIntentAnalysis(
                sentiment="Negative" if "quiet" not in text_lower else "Neutral",
                intent="Constructive Feedback",
                confidence=0.89,
                reason="Viewer pointed out a technical or audio issue constructively."
            )

        if any(w in text_lower for w in ["garbage", "idiot", "incompetent"]):
            return SentimentIntentAnalysis(
                sentiment="Negative",
                intent="Complaint",
                confidence=0.95,
                reason="Hostile negative commentary."
            )

        return SentimentIntentAnalysis(
            sentiment="Neutral",
            intent="General",
            confidence=0.85,
            reason="General viewer observation."
        )

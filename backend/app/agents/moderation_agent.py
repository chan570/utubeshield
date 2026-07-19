from app.models.schemas import RawComment, SpamAnalysis, ToxicityAnalysis, SentimentIntentAnalysis, ModerationDecisionAnalysis
from app.services.llm_factory import LLMFactory
from app.prompts.moderation_prompts import MODERATION_DECISION_PROMPT
from app.utils.logger import logger

class ModerationAgent:
    """
    Agent 5: Moderation Decision Agent
    Responsibilities:
    - Synthesize output from Spam, Toxicity, and Sentiment agents.
    - Return one of: Keep, Hide, Delete, Needs Human Review.
    - Provide clear rationale.
    """

    @staticmethod
    def decide(
        comment: RawComment,
        spam_res: SpamAnalysis,
        toxicity_res: ToxicityAnalysis,
        sentiment_res: SentimentIntentAnalysis
    ) -> ModerationDecisionAnalysis:

        llm = LLMFactory.get_llm()

        if llm:
            try:
                from langchain.prompts import PromptTemplate
                from langchain.output_parsers import PydanticOutputParser

                parser = PydanticOutputParser(pydantic_object=ModerationDecisionAnalysis)
                prompt = PromptTemplate(
                    template=MODERATION_DECISION_PROMPT + "\n{format_instructions}",
                    input_variables=[
                        "text", "author", "is_spam", "spam_confidence", "spam_reason",
                        "toxicity_category", "toxicity_severity", "toxicity_confidence",
                        "toxicity_reason", "sentiment", "intent", "sentiment_reason"
                    ],
                    partial_variables={"format_instructions": parser.get_format_instructions()}
                )

                chain = prompt | llm | parser
                res = chain.invoke({
                    "text": comment.text,
                    "author": comment.author,
                    "is_spam": spam_res.spam,
                    "spam_confidence": spam_res.confidence,
                    "spam_reason": spam_res.reason,
                    "toxicity_category": toxicity_res.category,
                    "toxicity_severity": toxicity_res.severity,
                    "toxicity_confidence": toxicity_res.confidence,
                    "toxicity_reason": toxicity_res.reason,
                    "sentiment": sentiment_res.sentiment,
                    "intent": sentiment_res.intent,
                    "sentiment_reason": sentiment_res.reason
                })
                return res
            except Exception as e:
                logger.warning(f"[ModerationAgent] LLM error: {e}. Falling back to decision matrix.")

        # Robust Decision Logic Matrix
        if spam_res.spam:
            if "crypto" in spam_res.reason.lower() or "telegram" in spam_res.reason.lower() or "giveaway" in spam_res.reason.lower():
                return ModerationDecisionAnalysis(
                    decision="Delete",
                    reason="Automatically deleted: High confidence scam or promotional financial spam."
                )
            return ModerationDecisionAnalysis(
                decision="Hide",
                reason="Hidden from public view: Bot-like or repetitive promotional text."
            )

        if toxicity_res.severity in ["High", "Severe"]:
            return ModerationDecisionAnalysis(
                decision="Delete",
                reason=f"Automatically deleted: Severe toxicity flag ({toxicity_res.category})."
            )
        elif toxicity_res.severity in ["Medium"]:
            return ModerationDecisionAnalysis(
                decision="Hide",
                reason=f"Hidden: Contains insulting or inappropriate language ({toxicity_res.category})."
            )
        elif toxicity_res.severity in ["Low"]:
            return ModerationDecisionAnalysis(
                decision="Needs Human Review",
                reason="Borderline comment: Flagged for minor offensive remarks requiring human moderator review."
            )

        return ModerationDecisionAnalysis(
            decision="Keep",
            reason="Approved: Comment complies with community guidelines."
        )

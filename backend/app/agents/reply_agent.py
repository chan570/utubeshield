from typing import Optional
from app.models.schemas import RawComment, SentimentIntentAnalysis, ReplyAnalysis
from app.services.llm_factory import LLMFactory
from app.prompts.reply_prompts import REPLY_GENERATOR_PROMPT
from app.utils.logger import logger

class ReplyAgent:
    """
    Agent 6: Reply Generator Agent
    Responsibilities:
    - Generate polite, concise AI replies ONLY for:
      Questions, Constructive Feedback, Feature Requests, Complaints.
    """

    SUPPORTED_INTENTS = {"Question", "Constructive Feedback", "Feature Request", "Complaint"}

    @classmethod
    def generate(
        cls,
        comment: RawComment,
        sentiment_res: SentimentIntentAnalysis,
        video_title: str = "Video"
    ) -> Optional[ReplyAnalysis]:

        if sentiment_res.intent not in cls.SUPPORTED_INTENTS:
            return None

        llm = LLMFactory.get_llm()

        if llm:
            try:
                from langchain.prompts import PromptTemplate
                from langchain.output_parsers import PydanticOutputParser

                parser = PydanticOutputParser(pydantic_object=ReplyAnalysis)
                prompt = PromptTemplate(
                    template=REPLY_GENERATOR_PROMPT + "\n{format_instructions}",
                    input_variables=["author", "intent", "text", "video_title"],
                    partial_variables={"format_instructions": parser.get_format_instructions()}
                )

                chain = prompt | llm | parser
                res = chain.invoke({
                    "author": comment.author,
                    "intent": sentiment_res.intent,
                    "text": comment.text,
                    "video_title": video_title
                })
                return res
            except Exception as e:
                logger.warning(f"[ReplyAgent] LLM error: {e}. Using intelligent template reply engine.")

        # Template-based Fallback Generator
        intent = sentiment_res.intent
        author = comment.author.split()[0] if comment.author else "there"

        if intent == "Question":
            return ReplyAnalysis(
                suggested_reply=f"Hi {author}! Thank you for watching. The source code repository and resources are linked in the video description box!",
                tone="Helpful"
            )
        elif intent == "Feature Request":
            return ReplyAnalysis(
                suggested_reply=f"Hi {author}! That's a fantastic suggestion. I've added this topic to our roadmap for upcoming videos!",
                tone="Grateful"
            )
        elif intent == "Constructive Feedback":
            return ReplyAnalysis(
                suggested_reply=f"Thanks for pointing that out, {author}! We appreciate the constructive feedback and will improve this in our next release.",
                tone="Professional"
            )
        elif intent == "Complaint":
            return ReplyAnalysis(
                suggested_reply=f"Hi {author}, we're sorry to hear about the issue! Please check our pinned comment or docs for troubleshooting steps.",
                tone="Empathetic"
            )

        return None

import re
from app.models.schemas import RawComment, SpamAnalysis
from app.services.llm_factory import LLMFactory
from app.prompts.spam_prompts import SPAM_DETECTION_PROMPT
from app.utils.logger import logger

class SpamAgent:
    """
    Agent 2: Spam Detection Agent
    Detects:
    - Promotional spam
    - Scam & Fraud (crypto, Telegram, WhatsApp)
    - Repeated messages
    - Fake giveaways
    - Bot-like comments
    """

    @staticmethod
    def analyze(comment: RawComment) -> SpamAnalysis:
        llm = LLMFactory.get_llm()

        if llm:
            try:
                from langchain.prompts import PromptTemplate
                from langchain.output_parsers import PydanticOutputParser
                
                parser = PydanticOutputParser(pydantic_object=SpamAnalysis)
                prompt = PromptTemplate(
                    template=SPAM_DETECTION_PROMPT + "\n{format_instructions}",
                    input_variables=["author", "text"],
                    partial_variables={"format_instructions": parser.get_format_instructions()}
                )
                
                chain = prompt | llm | parser
                res = chain.invoke({"author": comment.author, "text": comment.text})
                return res
            except Exception as e:
                logger.warning(f"[SpamAgent] LLM analysis error: {e}. Falling back to rule engine.")

        # Fallback Heuristic Rule Engine for Spam/Scam Detection
        text_lower = comment.text.lower()
        spam_keywords = ["telegram", "whatsapp", "crypto", "giveaway", "iphone", "guaranteed profits", "trading signals", "contact mr", "click link", "http", "www."]
        
        matched = [kw for kw in spam_keywords if kw in text_lower]
        if matched:
            return SpamAnalysis(
                spam=True,
                confidence=0.92,
                reason=f"Detected suspicious promotional/scam patterns: {', '.join(matched)}"
            )

        return SpamAnalysis(
            spam=False,
            confidence=0.95,
            reason="No spam, bot activity, or promotional scam triggers detected."
        )

from app.models.schemas import RawComment, ToxicityAnalysis
from app.services.llm_factory import LLMFactory
from app.prompts.toxicity_prompts import TOXICITY_DETECTION_PROMPT
from app.utils.logger import logger

class ToxicityAgent:
    """
    Agent 3: Toxicity Detection Agent
    Detects:
    - Toxicity
    - Harassment
    - Hate Speech
    - Threats
    - Offensive language
    """

    @staticmethod
    def analyze(comment: RawComment) -> ToxicityAnalysis:
        llm = LLMFactory.get_llm()

        if llm:
            try:
                from langchain.prompts import PromptTemplate
                from langchain.output_parsers import PydanticOutputParser

                parser = PydanticOutputParser(pydantic_object=ToxicityAnalysis)
                prompt = PromptTemplate(
                    template=TOXICITY_DETECTION_PROMPT + "\n{format_instructions}",
                    input_variables=["author", "text"],
                    partial_variables={"format_instructions": parser.get_format_instructions()}
                )

                chain = prompt | llm | parser
                res = chain.invoke({"author": comment.author, "text": comment.text})
                return res
            except Exception as e:
                logger.warning(f"[ToxicityAgent] LLM error: {e}. Falling back to rule engine.")

        # Fallback Rule Engine
        text_lower = comment.text.lower()
        toxic_terms = ["garbage", "idiot", "incompetent", "delete your channel", "hate", "stfu", "dumb"]
        matched = [t for t in toxic_terms if t in text_lower]

        if matched:
            return ToxicityAnalysis(
                category="Harassment",
                severity="High" if "idiot" in text_lower else "Medium",
                confidence=0.88,
                reason=f"Comment contains hostile/insulting language ({', '.join(matched)})."
            )

        return ToxicityAnalysis(
            category="None",
            severity="None",
            confidence=0.98,
            reason="Comment is clean and free of toxic or harassing material."
        )

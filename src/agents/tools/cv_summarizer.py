from src.agents.prompts.summarizing_prompt import SummarizingPrompt
from src.agents.schemas.cv_schema import CVParseResult
from pydantic import ValidationError
from src.models.model import Model
import json
import re


class CVSummarizer:
    @staticmethod
    def build_prompt(cv_text: str) -> str:
        """Builds the prompt for summarizing the CV content."""
        prompt = SummarizingPrompt.summarizing_prompt(cv_text)
        return prompt

    @staticmethod
    def summarization(cv_text: str) -> dict:
        """Summarizes the CV content using a language model."""
        prompt = CVSummarizer.build_prompt(cv_text)
        response = Model.ollama_model().invoke(prompt)

        if hasattr(response, "content"):
            response = response.content

        response = CVSummarizer._extract_json(str(response))

        try:
            parsed_response = json.loads(response)
            return CVParseResult.model_validate(parsed_response).model_dump()

        except (json.JSONDecodeError, ValidationError):
            return CVParseResult().model_dump()

    @staticmethod
    def _extract_json(response: str) -> str:
        """Extract JSON from a model response that may include markdown fences."""
        response = response.strip()

        if response.startswith("```"):
            response = re.sub(r"^```(?:json)?", "", response).strip()
            response = re.sub(r"```$", "", response).strip()

        return response

from src.agents.states.state import AgentState
from src.agents.tools.full_text import FullText
from src.agents.tools.cv_summarizer import CVSummarizer

class CVParsingNode:
    @staticmethod
    def cv_parsing_node(state: AgentState) -> AgentState:
        """This node is responsible for parsing the CV content and extracting relevant information."""

        try:
            payload = FullText.extract_document_payload(state["cv_path"])
        except (FileNotFoundError, ValueError) as error:
            state["cv_errors"] = [*state.get("cv_errors", []), str(error)]
            return state

        metadata = payload["metadata"]

        state["cv_name"] = metadata["file_name"]
        state["cv_metadata"] = metadata
        state["cv_content"] = payload["document_parts"]
        state["cv_raw_text"] = payload["full_text"]
        state["cv_number_of_pages"] = payload["parts_count"]
        state["cv_characters_count"] = payload["characters_count"]

        try:
            llm_result = CVSummarizer.summarization(state["cv_raw_text"])
            state["cv_summary"] = llm_result.get("summary", "")
            state["cv_data"] = llm_result.get("cv_data", {})
        except Exception as error:
            state["cv_errors"] = [*state.get("cv_errors", []), f"LLM parsing error: {str(error)}"]
            state["cv_summary"] = ""
            state["cv_data"] = {}
            return state

        state["cv_errors"] = []

        return state

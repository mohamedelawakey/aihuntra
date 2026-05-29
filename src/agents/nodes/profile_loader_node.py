from src.agents.states.state import AgentState
from src.utils.cleaner import DataCleaner


class ProfileLoaderNode:
    @staticmethod
    def profile_loader_node(state: AgentState) -> AgentState:
        """This node is responsible for loading the users' profile information"""
        
        state["name"] = DataCleaner.clean_name(state["name"])
        state["role"] = DataCleaner.clean_text(state["role"])
        state["email"] = DataCleaner.clean_email(state["email"])
        state["phone"] = DataCleaner.clean_phone(state["phone"])
        state["education"] = DataCleaner.clean_text(state["education"])
        state["profile"] = DataCleaner.clean_text(state["profile"])
        state["skills"] = DataCleaner.clean_list(state["skills"])
        state["languages"] = DataCleaner.clean_list(state["languages"])
        state["social_media_links"] = DataCleaner.clean_links(state["social_media_links"])

        return state

from src.agents.nodes.profile_loader_node import ProfileLoaderNode
from src.agents.nodes.cv_parsing_node import CVParsingNode
from langgraph.graph import START, END, StateGraph
from src.agents.states.state import AgentState


class Graph:
    @staticmethod
    def graph():
        graph = StateGraph(AgentState)

        # nodes
        graph.add_node("loader", ProfileLoaderNode.profile_loader_node)
        graph.add_node("cv_parser", CVParsingNode.cv_parsing_node)

        # edges
        graph.add_edge(START, "loader")
        graph.add_edge("loader", "cv_parser")
        graph.add_edge("cv_parser", END)

        app = graph.compile()

        return app

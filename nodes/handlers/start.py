from dataclasses import dataclass
from nodes.base import BaseNode, GraphState

@dataclass
class StartNode(BaseNode):
    label: str = "Start"
    def execute(self, state: GraphState) -> GraphState:
        try:
            super().execute(state)
            return state
        except Exception as e:
            raise RuntimeError(f"Error in StartNode: {e}") from e
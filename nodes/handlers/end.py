from dataclasses import dataclass
from nodes.base import BaseNode, GraphState

@dataclass(slots=True)
class EndNode(BaseNode):
    label: str = "End"

    def __post_init__(self):
        self.next = None

    def execute(self, state: GraphState) -> GraphState:
        try:
            self._log(state, 20, f"{__class__.__name__}[id={self.id}] starting ")
            self._log(state, 20, f"{__class__.__name__}[id={self.id}] completed ▶ Next[id={self.next}]")
            return state
        except Exception as e:
            super()._log(state, 40, f"Error in {__class__.__name__}: {e}")
            raise RuntimeError(f"Error in {__class__.__name__}: {e}") from e
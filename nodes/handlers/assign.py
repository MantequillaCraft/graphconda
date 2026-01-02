from dataclasses import dataclass
from nodes.base import BaseNode, GraphState
from typing import Any


@dataclass
class AssignNode(BaseNode):
    var_name: str = ""
    value: str = Any

    def execute(self, state: GraphState) -> GraphState:
        try:
            self._log(state, 20, f"{__class__.__name__}[id={self.id}] starting ")
            state.current_node_id = self.id
            state.vars[self.var_name] = self.value
            super().execute(state)
            self._log(state, 20, f"{__class__.__name__}[id={self.id}] completed ▶ Next[id={self.next}]")
            return state
        except Exception as e:
            raise RuntimeError(f"Error in AssignNode: {e}") from e
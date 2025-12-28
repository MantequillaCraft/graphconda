from dataclasses import dataclass
from nodes.base import BaseNode, GraphState
from typing import Any


@dataclass
class AssignNode(BaseNode):
    var_name: str = ""
    value: str = Any

    def execute(self, state: GraphState) -> GraphState:
        try:
            state.current_node_id = self.id
            state.vars[self.var_name] = self.value

            super().execute(state)
            return state
        except Exception as e:
            raise RuntimeError(f"Error in AssignNode: {e}") from e
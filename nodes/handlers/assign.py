from dataclasses import dataclass
from nodes.base import BaseNode, GraphState
from typing import Any

@dataclass(slots=True)
class AssignNode(BaseNode):
    var_name: str = ""
    value: str = Any

    def execute(self, state: GraphState) -> GraphState:
        state.current_node_id = self.id
        state.vars[self.var_name] = self.value
        state.last = self.value
        return state

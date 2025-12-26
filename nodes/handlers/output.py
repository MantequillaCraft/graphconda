from dataclasses import dataclass
from nodes.base import BaseNode, GraphState

@dataclass(slots=True)
class OutputNode(BaseNode):
    output: str = ""

    def execute(self, state: GraphState) -> GraphState:
        print(self.output)
        return state
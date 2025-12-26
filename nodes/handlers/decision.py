from dataclasses import dataclass
from nodes.base import BaseNode

@dataclass
class DecisionNode(BaseNode):
    label: str = "x" 
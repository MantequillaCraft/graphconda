from dataclasses import dataclass
from nodes.base import BaseNode

@dataclass
class EndNode(BaseNode):
    label: str = "End"
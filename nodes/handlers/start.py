from dataclasses import dataclass
from nodes.base import BaseNode

@dataclass(slots=True)
class StartNode(BaseNode):
    label: str = "Start"

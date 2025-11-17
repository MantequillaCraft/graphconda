from typing import List, Optional
from schema.Edge import Edge
from schema.Node import Node


class Flowchart():

    def __init__(self, nodes: List[str], edges: List[tuple], title: Optional[str] = None):
        self.nodes = nodes
        self.edges = edges
        self.title = title
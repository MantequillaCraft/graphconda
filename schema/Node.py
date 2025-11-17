from typing import List, Optional


class Node():

    def __init__ (self, node_id: str, kind: str, label: Optional[str] = None):
        self.node_id = node_id
        self.kind = kind
        self.label = label


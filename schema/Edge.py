from schema.Node import Node


class Edge():

    def __init__(self, id: str, source: Node, target: Node, label: str = ""):
        self.id = id
        self.source = source
        self.target = target
        self.label = label
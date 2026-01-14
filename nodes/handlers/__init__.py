from importlib import import_module
from typing import Type

# type_str -> "modulo:Clase"
# para nuevos NodeTypes agregalos aqui (((:
_NODE_MAP: dict[str, str] = {
    "start": "nodes.handlers.start:StartNode",
    "assign": "nodes.handlers.assign:AssignNode",
    "decision": "nodes.handlers.decision:DecisionNode",
    "input": "nodes.handlers.input:InputNode",
    "output": "nodes.handlers.output:OutputNode",
    "loop": "nodes.handlers.loop:LoopNode",
    "end": "nodes.handlers.end:EndNode",
    "operation": "nodes.handlers.operation:OperationNode",
}


def get_node_class(type_name: str) -> Type:
    path = _NODE_MAP[type_name]
    module_name, class_name = path.split(":")
    mod = import_module(module_name)
    return getattr(mod, class_name)

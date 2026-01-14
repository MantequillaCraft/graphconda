from importlib import import_module
from typing import Type

# type_str -> "modulo:Clase"
# para nuevos NodeTypes agregalos aqui (((:
_NODE_MAP: dict[str, str] = {
    "start": "core.nodes.start:StartNode",
    "assign": "core.nodes.assign:AssignNode",
    "decision": "core.nodes.decision:DecisionNode",
    "input": "core.nodes.input:InputNode",
    "output": "core.nodes.output:OutputNode",
    "loop": "core.nodes.loop:LoopNode",
    "end": "core.nodes.end:EndNode",
    "operation": "core.nodes.operation:OperationNode",
}


def get_node_class(type_name: str) -> Type:
    path = _NODE_MAP[type_name]
    module_name, class_name = path.split(":")
    mod = import_module(module_name)
    return getattr(mod, class_name)

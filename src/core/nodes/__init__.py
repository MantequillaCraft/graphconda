from importlib import import_module
from typing import Type

PATH = "src.core.nodes"
# type_str -> "modulo:Clase"
# para nuevos NodeTypes agregalos aqui (((:
_NODE_MAP: dict[str, str] = {
    "start": PATH + ".start:StartNode",
    "assign": PATH + ".assign:AssignNode",
    "decision": PATH + ".decision:DecisionNode",
    "input": PATH + ".input:InputNode",
    "output": PATH + ".output:OutputNode",
    "loop": PATH + ".loop:LoopNode",
    "end": PATH + ".end:EndNode",
    "operation": PATH + ".operation:OperationNode",
}


def get_node_class(type_name: str) -> Type:
    if type_name not in _NODE_MAP:
        raise ValueError(
            f"Unknown node type: '{type_name}'. Valid types: {list(_NODE_MAP.keys())}"
        )

    path = _NODE_MAP[type_name]
    module_name, class_name = path.split(":")

    try:
        mod = import_module(module_name)
        return getattr(mod, class_name)
    except ImportError as e:
        raise ImportError(f"Could not import module '{module_name}': {e}") from e
    except AttributeError as e:
        raise AttributeError(
            f"Class '{class_name}' does not exist in '{module_name}': {e}"
        ) from e

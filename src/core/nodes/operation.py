from dataclasses import dataclass
from src.core import BaseNode, GraphState
import ast
from src.core.helpers.operation import (
    OP,
)


@dataclass
class OperationNode(BaseNode):
    var_name: str = ""
    operation: str = ""

    def execute(self, state: GraphState) -> GraphState:
        try:
            self._log(state, 20, f"{__class__.__name__}[id={self.id}] starting ")

            expr = ast.parse(self.operation, mode="eval").body
            state.vars[self.var_name] = self._eval_operation_expr(
                node=expr, vars_dict=state.vars
            )

            state.current_node_id = self.id
            super().execute(state)
            self._log(
                state,
                20,
                f"{__class__.__name__}[id={self.id}] completed ▶ Next[id={self.next}]",
            )
            return state
        except Exception as e:
            raise RuntimeError(f"Error in AssignNode: {e}") from e

    def _eval_operation_expr(self, node, vars_dict: dict):
        # primero cargamos las variables del estado
        # Constantes: 123, "hola", True, None
        if isinstance(node, ast.Constant):
            return node.value

        # Variables: edad, nombre, etc.
        if isinstance(node, ast.Name):
            if node.id in vars_dict:
                return vars_dict[node.id]
            raise KeyError(f"Undefined variable: {node.id}")

        # Listas, tuplas, sets, dicts
        if isinstance(node, ast.List):
            return [self._eval_boolean_expr(e, vars_dict) for e in node.elts]
        if isinstance(node, ast.Tuple):
            return tuple(self._eval_boolean_expr(e, vars_dict) for e in node.elts)
        if isinstance(node, ast.Set):
            return {self._eval_boolean_expr(e, vars_dict) for e in node.elts}
        if isinstance(node, ast.Dict):
            return {
                self._eval_boolean_expr(k, vars_dict): self._eval_boolean_expr(
                    v, vars_dict
                )
                for k, v in zip(node.keys, node.values)
            }

        if isinstance(node, ast.BinOp):
            left = self._eval_operation_expr(node.left, vars_dict)
            right = self._eval_operation_expr(node.right, vars_dict)
            op = type(node.op)
            if op not in OP:
                raise ValueError(f"Unsupported operation: {op.__name__}")
            return OP[op](left, right)

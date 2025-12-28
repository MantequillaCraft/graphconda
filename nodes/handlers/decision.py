import ast
import operator

from dataclasses import dataclass
from nodes.base import BaseNode, GraphState

CMP = {
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
}

# TODO : 
#   - Soportar más tipos de datos (strings, floats, etc.)
#   - Soportar operaciones lógicas AND, OR, NOT
#   - Manejar errores y excepciones de manera más robusta

@dataclass
class DecisionNode(BaseNode):
    condition: str = "x"

    def execute(self, state: GraphState):
        try:
            vars = state.vars if state.vars is not None else {}
            self.condition = ast.parse(self.condition, mode="eval").body

            if not isinstance(self.condition, ast.Compare):
                raise ValueError("Only comparisons are supported (e.g. a < 10)")

            if isinstance(self.condition.left, ast.Constant):
                left = self.condition.left.value
            elif isinstance(self.condition.left, ast.Name):
                left = vars[self.condition.left.id]
            else:
                raise ValueError("Unsupported left side")

            op_type = type(self.condition.ops[0])
            if op_type not in CMP:
                raise ValueError(f"Unsupported operator: {op_type.__name__}")

            right_node = self.condition.comparators[0]
            if isinstance(right_node, ast.Constant):
                right = right_node.value
            elif isinstance(right_node, ast.Name):
                right = vars[right_node.id]
            else:
                raise ValueError("Unsupported right side")

            super().execute(state)
            return state , CMP[op_type](left, right)
        except Exception as e:
            raise RuntimeError(f"Error in DecisionNode: {e}") from e
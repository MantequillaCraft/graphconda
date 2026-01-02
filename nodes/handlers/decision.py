import ast
import operator
from dataclasses import dataclass
from nodes.base import BaseNode, GraphState


@dataclass(slots = True)
class DecisionNode(BaseNode):
    condition: str = ""

    def execute(self, state: GraphState[str]) -> GraphState:
        try:
            12312
            super()._log(state, 20, f"{__class__.__name__}[id={self.id}] starting ")
            # Parsea la condición como expresión Python
            expr = ast.parse(self.condition, mode="eval").body
            # Evalúa la expresión de forma segura
            result = bool(self._eval_boolean_expr(expr, state.vars))

            # Decide qué rama tomar según el resultado
            branch = "true" if result else "false"
            self.next = state.flow.get(self.id, {}).get(branch)
            super()._log(state, 20, f"{__class__.__name__}[id={self.id}] execution ▶ Next[id={self.next}]")

            # Guarda el resultado en el estado (opcional)
            state.last = result
            return state
        except Exception as e:
            super()._log(state, 40, f"Error in {__class__.__name__}: {e}")
            raise RuntimeError(f"Error in {__class__.__name__}: {e}") from e
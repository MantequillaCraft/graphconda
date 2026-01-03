import ast
from dataclasses import dataclass
from nodes.base import BaseNode, GraphState

from nodes.operators.boolean import (
    CMP,
    BOOL,
    UNARY,
    SAFE_STR_METHODS,
    SAFE_GLOBAL_FUNCS
)

@dataclass(slots = True)
class DecisionNode(BaseNode):
    condition: str = ""

    def execute(self, state: GraphState) -> GraphState:
        try:
            self._log(state, 20, f"{__class__.__name__}[id={self.id}] starting ")
            # Parsea la condición como expresión Python
            expr = ast.parse(self.condition, mode="eval").body
            # Evalúa la expresión de forma segura
            result = bool(self._eval_boolean_expr(expr, state.vars))

            # Decide qué rama tomar según el resultado
            branch = "true" if result else "false"
            self.next = state.flow.get(self.id, {}).get(branch)
            self._log(state, 20, f"{__class__.__name__}[id={self.id}] execution ▶ Next[id={self.next}]")

            # Guarda el resultado en el estado (opcional)
            state.last = result
            return state
        except Exception as e:
            super()._log(state, 40, f"Error in {__class__.__name__}: {e}")
            raise RuntimeError(f"Error in {__class__.__name__}: {e}") from e
    
    def _eval_boolean_expr(self, node, vars_dict: dict):
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
                self._eval_boolean_expr(k, vars_dict): self._eval_boolean_expr(v, vars_dict)
                for k, v in zip(node.keys, node.values)
            }

        # -------------------- Expresiones --------------------
        # Expresiones booleanas simples
        if isinstance(node, ast.Expr):
            return bool(self._eval_boolean_expr(node.value, vars_dict))

        # Operadores unarios: not x, -x, +x
        if isinstance(node, ast.UnaryOp):
            op = type(node.op)
            if op not in UNARY:
                raise ValueError(f"Unsupported unary op: {op.__name__}")
            return UNARY[op](self._eval_boolean_expr(node.operand, vars_dict))

        # Operadores booleanos: x and y, x or y
        if isinstance(node, ast.BoolOp):
            op = type(node.op)
            if op not in BOOL:
                raise ValueError(f"Unsupported boolean op: {op.__name__}")
            values = [bool(self._eval_boolean_expr(v, vars_dict)) for v in node.values]
            return BOOL[op](values)

        # Comparaciones: a < b, x == y, etc. (soporta cadenas: a < b < c)
        if isinstance(node, ast.Compare):
            left = self._eval_boolean_expr(node.left, vars_dict)
            for op_node, comp in zip(node.ops, node.comparators):
                op_type = type(op_node)
                if op_type not in CMP:
                    raise ValueError(f"Unsupported comparator: {op_type.__name__}")
                right = self._eval_boolean_expr(comp, vars_dict)
                if not CMP[op_type](left, right):
                    return False
                left = right
            return True

        # Llamadas a funciones y métodos
        if isinstance(node, ast.Call):
            # Funciones globales: len(x), int(x), etc.
            if isinstance(node.func, ast.Name):
                fn_name = node.func.id
                if fn_name not in SAFE_GLOBAL_FUNCS:
                    raise ValueError(f"Function not allowed: {fn_name}")
                args = [self._eval_boolean_expr(a, vars_dict) for a in node.args]
                return SAFE_GLOBAL_FUNCS[fn_name](*args)

            # Métodos de objetos: texto.islower(), texto.strip(), etc.
            if isinstance(node.func, ast.Attribute):
                obj = self._eval_boolean_expr(node.func.value, vars_dict)
                method = node.func.attr

                # Solo permitimos métodos en strings
                if isinstance(obj, str):
                    if method not in SAFE_STR_METHODS:
                        raise ValueError(f"String method not allowed: {method}")
                    m = getattr(obj, method)
                    args = [self._eval_boolean_expr(a, vars_dict) for a in node.args]
                    return m(*args)

                raise ValueError(f"Method calls not allowed for type: {type(obj).__name__}")

            raise ValueError("Unsupported call")

        # Bloqueamos acceso a atributos (previene __class__, __dict__, etc.)
        if isinstance(node, ast.Attribute):
            raise ValueError("Attribute access is not allowed (only method calls on whitelisted types)")

        raise ValueError(f"Unsupported expression node: {type(node).__name__}")
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import logging, time
import ast

from nodes.operators.boolean import (
    CMP,
    BOOL,
    UNARY,
    SAFE_STR_METHODS,
    SAFE_GLOBAL_FUNCS
)

LOGGER  = logging.getLogger(__name__)

# TODO :    
#   - Agregar manejo de logs en GraphState y en los nodos para registrar eventos importantes.
#   - NodeTypes faltantes: InputNode, FunctionNode, LoopNode, APINode, etc.



@dataclass
class GraphState:
    """
        GraphState representa el estado global de la ejecución del grafo de nodos.
        Sirve para mantener y pasar información relevante entre los nodos durante la ejecución.
        Esto esta basado en AgentState de LangChain, pero adaptado a nuestro contexto.

        Argumentos:
            vars: Diccionario que almacena las variables del programa.
            last: Último valor evaluado o calculado.
            logs: Lista opcional para almacenar mensajes de log o historial de ejecución.
            current_node_id: Identificador del nodo actualmente en ejecución, útil para depuración y seguimiento
        
    """
    vars: Dict[str, Any] = field(default_factory=dict)                          # variables del programa
    last: Any = None                                                            # último valor calculado
    current_node_id: Optional[str] = None                                       # debug/tracking
    time: float = time.time()                                                   # tiempo total de ejecución
    logs_enabled: bool = field(default_factory=lambda: True)                    # para el funcionamiento de logs
    logs: List[str] = field(default_factory=list)                               # bufer de los logs del 
    flow: Dict[str, str] = field(default_factory=dict)                          # flujo de nodos


@dataclass(slots=True)
class BaseNode:
    """
        BaseNode es la clase base para todos los nodes del flowchart.
        Proporciona una estructura común y funcionalidad básica que todos los nodos deben tener.

        Argumentos:
            id: Identificador único del nodo.
            next_id: Identificador del siguiente nodo a ejecutar (si aplica).
    """
    id: str
    next: dict[str, str] | str | None = None
    node_type: str = None

    def execute(self, state: GraphState) -> GraphState:
        """Ejecuta el nodo y actualiza el estado"""
        self.next = state.flow.get(self.id)
        return state

    def _log(self, state: GraphState, level: int, message: str) -> None:
        """ 
            Metodo para guardar y desplegar logs dentro de BaseNode Class y sus Class hijos
            
            Args:
                log_lvl: Entero, generalmente se le manda logging.INFO (estos son enteros logging.INFO = 20)
                log_text: Mensaje que se guardara y mostrara 
        """
        if not state.logs_enabled:
            return
        
        state.logs.append(message)
        LOGGER.log(level, message)


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

print()
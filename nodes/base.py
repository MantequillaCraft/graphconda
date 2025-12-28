from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

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
    time: float = 0.0                                                           # tiempo total de ejecución

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
        state.current_node_id = self.id
        return state
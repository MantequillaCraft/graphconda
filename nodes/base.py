from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class GraphState:
    """
        GraphState representa el estado global de la ejecución del grafo de nodos.
        Sirve para mantener y pasar información relevante entre los nodos durante la ejecución.
        Esto esta basado en AgentState de LangChain, pero adaptado a nuestro contexto.

        Argumentos:
            vars: Diccionario que almacena las variables del programa.
            last: Último valor evaluado o calculado.
            logs: Lista opcional para almacenar mensajes de log o historial de ejecución.
            halted: Indicador booleano que señala si la ejecución ha sido detenida por algún nodo.
            current_node_id: Identificador del nodo actualmente en ejecución, útil para depuración y seguimiento
        
    """
    vars: Dict[str, Any] = field(default_factory=dict)      # variables del programa
    last: Any = None                                        # último valor calculado
    logs: List[str] = field(default_factory=list)           # opcional
    halted: bool = False                                    # por si un nodo detiene
    current_node_id: Optional[str] = None                   # debug/tracking


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

    def execute(self, state: GraphState) -> GraphState:
        state.current_node_id = self.id
        return state
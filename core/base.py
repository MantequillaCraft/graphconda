import logging
import time

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

LOGGER = logging.getLogger(__name__)

# TODO :
#   - NodeTypes faltantes: InputNode, FunctionNode, LoopNode, APINode, etc.


@dataclass
class GraphState:
    """
    GraphState representa el estado global de la ejecución del grafo de nodos.
    Sirve para mantener y pasar información relevante entre los nodos durante la ejecución.
    Esto esta basado en AgentState de LangChain, pero adaptado a nuestro contexto.

    Attr:
        - `vars`: Diccionario que almacena las variables del programa.
        - `last`: Último valor evaluado o calculado.
        - `logs`: Lista opcional para almacenar mensajes de log o historial de ejecución.
        - `current_node_id`: Identificador del nodo actualmente en ejecución, útil para depuración y seguimiento

    """

    vars: Dict[str, Any] = field(default_factory=dict)  # variables del programa
    current_node_id: Optional[str] = None  # debug/tracking
    time: float = field(default_factory=time.time)  # tiempo total de ejecución

    logs_enabled: bool = False  # para el funcionamiento de logs
    logs: List[str] = field(default_factory=list)  # bufer de los logs del

    flow: Dict[str, str | dict] = field(default_factory=dict)  # flujo de nodos


@dataclass(slots=True)
class BaseNode:
    """
    BaseNode es la clase base para todos los nodes del flowchart.
    Proporciona una estructura común y funcionalidad básica que todos los nodos deben tener.

    Attr:
        - id: Identificador único del nodo.
        - next: Identificador del siguiente nodo a ejecutar (si aplica).
        - node_type: Ayuda a identificar el typo de nodo que se esta procesando
    """

    id: str
    next: str | Dict[str, str | None] | None = field(default=None)
    node_type: Optional[str] = field(default=None)

    def execute(self, state: GraphState) -> GraphState:
        """
        Ejecuta el nodo y actualiza el estado

        Args:

        """
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

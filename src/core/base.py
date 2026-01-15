import logging

from dataclasses import dataclass, field
from typing import Dict, Optional
from src.core import GraphState

LOGGER = logging.getLogger(__name__)

# TODO :
#   - NodeTypes faltantes: InputNode, FunctionNode, LoopNode, APINode, etc.


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

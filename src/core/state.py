import logging
import time

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

LOGGER = logging.getLogger(__name__)


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

import time
import logging
import json
import yaml

from dataclasses import dataclass, field
from typing import Dict, Any
from pathlib import Path

from nodes.base import GraphState
from nodes.handlers import get_node_class

LOGGER = logging.getLogger(__name__)

# TODO :
#   - NodeTypes faltantes: InputNode, FunctionNode, LoopNode, APINode, etc.


@dataclass(slots=True)
class Flowchart:
    """
    Representa un diagrama de flujo listo para ejecutarse.

    Attr:
        - `nodes`: definicion cruda (dict) leida desde YAML/JSON.
        - `metadata`: configuracion extra (por ejemplo delay entre nodos).
        - `flow`: conexiones entre nodos (next). Puede ser:
            - "A" -> "B" (lineal)
            - "A" -> {"true": "B", "false": "C"} (ramificacion)
            - "A" -> None (fin)

        En runtime construye:
        - `node_instances`: instancias reales de nodos (BaseNode y derivados).
        - `state`: GraphState que guarda variables/tiempo/logs durante la ejecucion.
    """

    # -------------------- data  --------------------
    nodes: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    flow: Dict[str, str | Dict[str, str] | None] = field(default_factory=dict)

    # -------------------- runtime --------------------
    node_instances: Dict[str, object] = field(init=False, default_factory=dict)
    state: "GraphState" = field(init=False)

    def __post_init__(self):
        """
        Inicializa estructuras de runtime.

        Raises:
            RuntimeError: Si falla la inicializacion del estado.
        """
        try:
            self.node_instances = {}
            self.state = GraphState(
                flow=self.flow, logs_enabled=self.metadata.get("logs_enabled")
            )
        except Exception as e:
            raise RuntimeError(f"Error initializing Flowchart: {e}") from e

    @staticmethod
    def load_flowchart(file_path: str) -> dict:
        """
        Carga un flowchart desde JSON o YAML segun la extension.

        Args:
            file_path: Ruta al archivo `.json`, `.yaml` o `.yml`.

        Returns:
            tuple[dict, str]: (data, name) donde `data` es el dict cargado y `name`
            es el nombre del archivo sin extension.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            ValueError: Si el formato no es soportado.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"El archivo '{file_path}' no existe")

        suffix = path.suffix.lower()

        with open(path, "r", encoding="utf-8") as f:
            if suffix == ".json":
                return json.load(f), path.stem
            elif suffix in (".yaml", ".yml"):
                return yaml.safe_load(f), path.stem
            else:
                raise ValueError(
                    f"Formato no soportado: '{suffix}'. Usa .json, .yaml o .yml"
                )

    def build_nodes(self):
        """
        Instancia todos los nodos definidos en `self.nodes` y los guarda en `self.node_instances`.

        Raises:
            RuntimeError: Si no se puede resolver el tipo del nodo o si los params no
            coinciden con el constructor del nodo.
        """
        try:
            for node_id, node_data in self.nodes.items():
                NodeCls = get_node_class(node_data["type"])
                params = node_data.get("params", {})

                self.node_instances[str(node_id)] = NodeCls(
                    id=str(node_id), node_type=node_data["type"], **params
                )

        except Exception as e:
            LOGGER.error(f"Error during node building: {e}")
            raise RuntimeError(f"Error during node building: {e}") from e

    def execution(self, start_id: str = "0") -> GraphState:
        """
        Ejecuta el flowchart desde `start_id` avanzando por `node.next` hasta None.

        Args:
            start_id: ID del nodo inicial.

        Returns:
            GraphState: Estado final con variables/logs y `time` como tiempo total de ejecucion.

        Raises:
            RuntimeError: Si falla la ejecucion de un nodo o el grafo esta mal conectado.
            KeyError: Si `start_id` o algun `next` no existe en `self.node_instances`.
        """
        try:
            state = self.state
            delay = self.metadata.get("delay_time", 0) / 1000.0  # ms -> s
            time_started = time.time()

            current = start_id
            while current:
                node = self.node_instances[current]
                node.execute(state)
                current = node.next

                if delay > 0:
                    time.sleep(delay)
                    state.time += delay

            state.time = time.time() - time_started
            return state

        except Exception as e:
            LOGGER.error(f"Error during execution: {e}")
            raise RuntimeError(f"Error during execution: {e}") from e

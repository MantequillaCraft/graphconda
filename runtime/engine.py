import time, logging

from nodes.base import GraphState
from nodes.handlers import get_node_class

LOGGER = logging.getLogger(__name__)

# TODO :    
#   - Agregar manejo de logs en Flowchart y en los nodos para registrar eventos importantes.
#   - NodeTypes faltantes: InputNode, FunctionNode, LoopNode, APINode, etc.


def SafeModeExecution(flowchart_json: dict, start_id="0") -> GraphState:
    """
    Ejecuta el diagrama de flujo comenzando desde el nodo con ID `start_id`.

    Args:
        flowchart_json (dict): Representación JSON del diagrama de flujo.
        nodes (dict): Diccionario de instancias de nodos, donde las claves son los IDs de los nodos.
        start_id (str): ID del nodo desde el cual comenzar la ejecución.
    Returns:
        GraphState: El estado final del grafo después de la ejecución.
    """

    try:
        nodes_json: dict = flowchart_json["nodes"]

        instances: dict[str, object] = {}

        for i, node_data in nodes_json.items():
            NodeCls = get_node_class(node_data["type"])

            node_id: str = i
            params = node_data.get("params", {})

            instances[node_id] = NodeCls(id=node_id, node_type=node_data["type"], **params)

    except Exception as e:
        LOGGER.error(f"Error during node instantiation: {e}")
        raise RuntimeError(f"Error during node instantiation: {e}") from e
    finally:
        state = GraphState()  # Estado inicial del grafo
        delay = flowchart_json.get("metadata", {}).get("delay_time", 0) / 1000.0  # Retardo entre nodos en segundos
        state.flow = flowchart_json["next"]  # Mapa de transiciones entre nodos
        time_started = time.time()  # Tiempo de inicio de la ejecución

        current = start_id
        while current:
            node = instances[current]

            node.execute(state)

            current = node.next

            if delay > 0:
                time.sleep(delay)
                state.time += delay

        state.time = time.time() - time_started
        return state
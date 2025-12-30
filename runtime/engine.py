import time, logging

from nodes.base import GraphState
from nodes.handlers import get_node_class

LOGGER = logging.getLogger(__name__)


# TODO: Maybe estaria chevere, hacer una clase FLowchart.
#       con dos metodos SafeModeExecution y DebugModeExecution
def SafeModeExecution(flowchart_json: dict) -> GraphState:
    """
        Ejecuta el diagrama de flujo comenzando desde el nodo con ID `start_id`.

        Args:
            flowchart_json (dict): Representación JSON del diagrama de flujo.
        Returns:
            GraphState: El estado final del grafo después de la ejecución.
    """
    state = GraphState()                                                            # Estado inicial del grafo
    delay = flowchart_json.get("metadata", {}).get("delay_time", 0) / 1000.0        # Retardo entre nodos en segundos
    state.flow = flowchart_json["next"]                                             # Mapa de transiciones entre nodos                                                    # Tiempo de inicio de la ejecución

    nodes_json: dict = flowchart_json["nodes"]

    instances: dict[str, object] = {}

    for i, node_data in nodes_json.items():
        try:
                NodeCls = get_node_class(node_data["type"])

                node_id: str = i
                params = node_data.get("params", {})

                instances[node_id] = NodeCls(id=node_id, node_type=node_data["type"], **params)

        except Exception as e:
            LOGGER.error(f"Error during node instantiation: {e}")
            raise RuntimeError(f"Error during node instantiation: {e}") from e
        finally:
            instances[node_id] = instances[node_id]
            result = instances[node_id].execute(state)
            state = result if isinstance(result, GraphState) else state
            
            if delay > 0:
                time.sleep(delay)
                state.time += delay


    state.time = time.time() - state.time
    return state
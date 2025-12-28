import time

from nodes.base import GraphState
from nodes.handlers import get_node_class


def run_flowchart(flowchart_json: dict, nodes: dict, start_id: str = "0") -> GraphState:
    """
        Ejecuta el diagrama de flujo comenzando desde el nodo con ID `start_id`.

        Args:
            flowchart_json (dict): Representación JSON del diagrama de flujo.
            nodes (dict): Diccionario de instancias de nodos, donde las claves son los IDs de los nodos.
            start_id (str): ID del nodo desde el cual comenzar la ejecución.
        Returns:
            GraphState: El estado final del grafo después de la ejecución.
    """
    state = GraphState()                                                            # Estado inicial del grafo
    delay = flowchart_json.get("metadata", {}).get("delay_time", 0) / 1000.0        # Retardo entre nodos en segundos
    next_map = flowchart_json["next"]                                               # Mapa de transiciones entre nodos  
    time_started = time.time()                                                      # Tiempo de inicio de la ejecución

    current = start_id
    while current:
        node = nodes[current]
        
        result = node.execute(state) if hasattr(node, "execute") else state
        
        if isinstance(result, tuple):
            state, condition = result
            current = next_map[current].get("true" if condition else "false")
        else:
            state = result
            nxt = next_map.get(current)
            current = nxt if isinstance(nxt, str) else None
        
        if delay > 0:
            time.sleep(delay)
            state.time += delay
    
    state.time = time.time() - time_started
    return state


def build_nodes(flowchart_json: dict) -> dict[str, object]:
    nodes_json: dict = flowchart_json["nodes"]

    instances: dict[str, object] = {}

    for i, node_data in nodes_json.items():
        NodeCls = get_node_class(node_data["type"])

        node_id: str = i
        params = node_data.get("params", {})

        instances[node_id] = NodeCls(id=node_id, node_type=node_data["type"], **params)

    return instances
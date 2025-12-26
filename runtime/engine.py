from nodes.base import GraphState

def run_flowchart(
    flowchart_json: dict, 
    nodes: dict[str, object], 
    start_id: str = "0"
) -> GraphState:
    state = GraphState()
    next_map = flowchart_json.get("next", {})

    current = start_id
    while current is not None:
        node = nodes[current]

        # Ejecuta el nodo (si existe)
        if hasattr(node, "execute"):
            state = node.execute(state)
        else:
            print(f"[SKIP] Node {current} has no execute()")

        # Avanza al siguiente
        nxt = next_map.get(current)

        # Por ahora, solo lineal (string o None)
        if isinstance(nxt, dict):
            print(f"[STOP] Branching not handled yet at node {current}: {nxt}")
            break

        current = nxt
    return state

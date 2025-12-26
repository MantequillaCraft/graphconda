from nodes.handlers import get_node_class

def build_nodes(flowchart_json: dict) -> dict[str, object]:
    nodes_json: dict = flowchart_json["nodes"]

    instances: dict[str, object] = {}

    for i, node_data in nodes_json.items():
        NodeCls = get_node_class(node_data["type"])

        node_id: str = i
        params = node_data.get("params", {})
        
        instances[node_id] = NodeCls(id=node_id, **params)

    return instances
import json
from runtime.engine import run_flowchart, build_nodes

# TODO: 
#   - Diferenciacion entre SafeModeExecution y RealTimeExecution
#   - Configurar el logging para registrar la ejecución del diagrama de flujo

flowchart_json = json.load(open("examples/example2.json", "r"))

nodes = build_nodes(flowchart_json)
run_flowchart(flowchart_json, nodes, start_id="0")

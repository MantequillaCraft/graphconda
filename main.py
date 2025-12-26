import json
from runtime.builtins import build_nodes
from runtime.engine import run_flowchart  # donde lo pongas

flowchart_json = json.load(open("examples/example2.json", "r"))

nodes = build_nodes(flowchart_json)
run_flowchart(flowchart_json, nodes, start_id="0")

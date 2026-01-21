import argparse
import logging

from pathlib import Path

from src.utils import setup_logging
from src.core import Flowchart
from src.ui import app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ejecuta un diagrama de flujo desde un archivo JSON o YAML"
    )
    parser.add_argument(
        "-v",
        "--visual",
        action="store_true"
    )
    if not parser.parse_known_args()[0].visual:
        parser.add_argument(
            "file", type=Path, help="Ruta al archivo del flowchart (.json, .yaml, .yml)"
        )


    args = parser.parse_args()

    try:
        if args.visual:
            app.MainWindow()
        else:
            flowchart_dict, file_name = Flowchart.load_flowchart(args.file)
            setup_logging(log_level=logging.INFO, log_file=f"logs/{file_name}.log")
            flowchart = Flowchart(
                nodes=flowchart_dict.get("nodes"),
                metadata=flowchart_dict.get("metadata"),
                flow=flowchart_dict.get("next"),
            )

            flowchart.build_nodes()

            result = flowchart.execution()

            print(result)
    except Exception as e:
        raise SystemExit(f"Error: {e}")

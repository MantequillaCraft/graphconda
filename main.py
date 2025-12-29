import argparse, json, yaml
import logging

from pathlib import Path

from utils.logging_config import setup_logging
from runtime.engine import run_flowchart, build_nodes


# TODO: 
#   - Diferenciacion entre SafeModeExecution y RealTimeExecution
#   - Configurar el logging para registrar la ejecución del diagrama de flujo


def load_flowchart(file_path: str) -> dict:
    """Carga un flowchart desde JSON o YAML según la extensión."""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"El archivo '{file_path}' no existe")
    
    suffix = path.suffix.lower()
    
    with open(path, 'r') as f:
        if suffix == '.json':
            return json.load(f) , path.name.strip(suffix)
        elif suffix in ['.yaml', '.yml']:
            return yaml.safe_load(f), path.name.strip(suffix)
        else:
            raise ValueError(
                f"Formato no soportado: '{suffix}'. "
                "Usa .json, .yaml o .yml"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ejecuta un diagrama de flujo desde un archivo JSON o YAML"
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Ruta al archivo del flowchart (.json, .yaml, .yml)"
    )
    
    args = parser.parse_args()
    
    try:
        flowchart, file_name = load_flowchart(args.file)
        setup_logging(
            log_level=logging.INFO,  # Cambia a DEBUG para más detalle
            log_file=f"logs/{file_name}.log"  # Opcional: guarda logs en archivo
        )
        nodes = build_nodes(flowchart)
        run_flowchart(flowchart, nodes, start_id="0")
    except Exception as e:
        raise SystemExit(f"Error: {e}")
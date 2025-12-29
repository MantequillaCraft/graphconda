import argparse, json, yaml

from pathlib import Path

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
            return json.load(f)
        elif suffix in ['.yaml', '.yml']:
            return yaml.safe_load(f)
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
        flowchart = load_flowchart(args.file)
        nodes = build_nodes(flowchart)
        run_flowchart(flowchart, nodes, start_id="0")
    except Exception as e:
        raise SystemExit(f"Error: {e}")
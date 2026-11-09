from pathlib import Path

def asset_path(name):
    return str(Path(__file__).resolve().parent / name)

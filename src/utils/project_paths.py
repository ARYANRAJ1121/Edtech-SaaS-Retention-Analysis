from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
ADVANCED_DATA_DIR = DATA_DIR / "advanced"
ARTIFACTS_DIR = SRC_DIR / "models" / "artifacts"


def project_path(*parts: str) -> Path:
    return PROJECT_ROOT.joinpath(*parts)


def data_path(*parts: str) -> Path:
    return DATA_DIR.joinpath(*parts)


def advanced_data_path(*parts: str) -> Path:
    return ADVANCED_DATA_DIR.joinpath(*parts)


def artifacts_path(*parts: str) -> Path:
    return ARTIFACTS_DIR.joinpath(*parts)

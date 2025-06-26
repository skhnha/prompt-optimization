import json
from pathlib import Path

def load_testset(path: str = "tests/testset.json") -> list[dict]:
    full_path = Path(path)
    if not full_path.exists():
        raise FileNotFoundError(f"테스트셋 파일이 존재하지 않습니다: {full_path}")
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)
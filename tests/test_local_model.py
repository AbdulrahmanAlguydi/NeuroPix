import ast
from pathlib import Path


def test_local_model_uses_fourteen_inference_steps():
    """The local model should use fewer steps to keep full-HD requests practical."""
    server_path = Path(__file__).resolve().parents[1] / "local_model" / "server.py"
    tree = ast.parse(server_path.read_text(encoding="utf-8"))

    steps = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for keyword in node.keywords:
            if keyword.arg == "num_inference_steps" and isinstance(
                keyword.value, ast.Constant
            ):
                steps.append(keyword.value.value)

    assert steps == [14]

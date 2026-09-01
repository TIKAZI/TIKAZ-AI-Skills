import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "suites" / "context-economy" / "context-orchestrator" / "scripts" / "route_context.py"


def load_router():
    spec = importlib.util.spec_from_file_location("route_context", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class ContextOrchestratorTests(unittest.TestCase):
    def test_valid_on_prefix_routes_to_onpremise_and_is_removed(self) -> None:
        router = load_router()
        for request, task in (
            ("ON", ""),
            ("ON analyze this PDF", "analyze this PDF"),
            ("ON: analyze video", "analyze video"),
            ("  ON：处理表格", "处理表格"),
        ):
            self.assertEqual(router.route_request(request), {"mode": "onpremise", "task": task})

    def test_false_positive_forms_stay_on_economy(self) -> None:
        router = load_router()
        for request in ("on file", "ONLY", "ON-board", "请 ON 分析", "turn ON vision"):
            self.assertEqual(router.route_request(request)["mode"], "economy")


if __name__ == "__main__":
    unittest.main()

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).parents[1]


class MatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = json.loads((ROOT / "matrix/compatibility.json").read_text(encoding="utf-8"))

    def test_current_sources_and_features(self):
        self.assertEqual(self.matrix["checked"], "2026-10-07")
        self.assertEqual(set(self.matrix["sources"]), {"provider_routing", "prompt_caching", "response_caching", "message_transforms", "video", "argolink_catalog"})
        for feature in ("provider_routing", "reasoning", "prompt_caching", "transforms", "video", "usage"):
            self.assertIn("openrouter", self.matrix["features"][feature])
            self.assertIn("argolink", self.matrix["features"][feature])

    def test_video_contract_is_explicit(self):
        argo = self.matrix["features"]["video"]["argolink"]
        self.assertEqual(argo["status_values"], ["pending", "done", "failed", "expired"])
        self.assertNotIn("running", argo["status_values"])
        self.assertIn("/v1/videos/generations", argo["submit"])

    def test_no_retired_base_or_boolean_shortcuts(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("api." + "argolink.io", text)
        self.assertNotIn("api." + "argolink.io", json.dumps(self.matrix))
        self.assertNotIn('"openrouter": true', json.dumps(self.matrix).lower())


if __name__ == "__main__":
    unittest.main()

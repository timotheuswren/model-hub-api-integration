import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))
from examples.requests import build_argolink_request, build_huggingface_request


class HubTests(unittest.TestCase):
    def test_readme_documents_both_contracts(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for term in ("Hugging Face", "Inference Providers", "DeepSeek", "GLM", "Qwen", "ArgoLink", "2026-10-07"):
            self.assertIn(term, text)
        self.assertIn("huggingface.co/docs/inference-providers/tasks/chat-completion", text)
        self.assertIn("huggingface.co/docs/inference-providers/pricing", text)
        self.assertNotIn("/v1/" + "tasks", text)

    def test_payloads_are_different_and_secret_safe(self):
        hf = build_huggingface_request("hello")
        argo = build_argolink_request("hello")
        self.assertIn("router.huggingface.co/v1", hf["url"])
        self.assertEqual(argo["json"]["model"], "glm-5.3")
        self.assertIn("${", argo["headers"]["Authorization"])
        with self.assertRaises(ValueError):
            build_argolink_request(" ")


if __name__ == "__main__":
    unittest.main()

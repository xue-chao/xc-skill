import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "transcribe", Path(__file__).with_name("transcribe.py"))
transcribe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transcribe)


class TranscribeTest(unittest.TestCase):
    def test_explicit_model_wins(self):
        self.assertEqual(transcribe.resolve_model("zh", "/tmp/m.bin"), Path("/tmp/m.bin"))

    def test_default_model_per_lang(self):
        self.assertEqual(transcribe.resolve_model("en", None).name, "ggml-small.en.bin")
        self.assertEqual(transcribe.resolve_model("zh", None).name, "ggml-large-v3-turbo.bin")

    def test_models_https_only(self):
        for _, url in transcribe.MODELS.values():
            self.assertTrue(url.startswith("https://"))

    def test_download_rejects_http(self):
        with self.assertRaises(SystemExit):
            transcribe.download("http://example.com/m.bin", Path("/tmp/m.bin"), None)


if __name__ == "__main__":
    unittest.main()
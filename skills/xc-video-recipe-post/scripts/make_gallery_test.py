import base64
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("make_gallery.py")
TINY_JPEG = base64.b64decode(
    "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0a"
    "HBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAABAAEBAREA/8QAFAABAAAAAAAA"
    "AAAAAAAAAAAACf/EABQQAQAAAAAAAAAAAAAAAAAAAAD/2gAIAQEAAD8AKp//2Q==")


class MakeGalleryTest(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.addCleanup(self.td.cleanup)
        self.a = Path(self.td.name) / "a.jpg"
        self.b = Path(self.td.name) / "b.jpg"
        self.a.write_bytes(TINY_JPEG)
        self.b.write_bytes(TINY_JPEG)

    def run_script(self, *extra):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--out", str(Path(self.td.name) / "g.html"),
             "--title", "t", "--img", str(self.a), "--cap", "甲",
             "--img", str(self.b), "--cap", "乙", *extra],
            capture_output=True, text=True)

    def test_build_embeds_base64(self):
        r = self.run_script("--no-compress")
        self.assertEqual(r.returncode, 0, r.stderr)
        page = (Path(self.td.name) / "g.html").read_text()
        self.assertEqual(page.count("data:image/jpeg;base64,"), 2)
        self.assertIn("甲", page)
        self.assertIn("乙", page)

    def test_over_limit_fails(self):
        r = self.run_script("--no-compress", "--max-bytes", "10")
        self.assertNotEqual(r.returncode, 0)

    def test_mismatched_counts_fail(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPT), "--out", "x.html",
             "--img", str(self.a), "--cap", "a", "--cap", "b"],
            capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
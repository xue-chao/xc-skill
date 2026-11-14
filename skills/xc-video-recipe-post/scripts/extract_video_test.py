import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("extract_video.py")
HAVE_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg/ffprobe not installed")
class ExtractVideoTest(unittest.TestCase):
    def test_extract(self):
        with tempfile.TemporaryDirectory() as td:
            video = Path(td) / "in.mp4"
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error",
                 "-f", "lavfi", "-i", "testsrc=duration=2:size=320x240:rate=10",
                 "-f", "lavfi", "-i", "anullsrc=r=16000:cl=mono",
                 "-t", "2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
                 str(video)], check=True, capture_output=True)
            out = Path(td) / "out"
            r = subprocess.run(
                [sys.executable, str(SCRIPT), str(video), str(out),
                 "--frame-interval", "1", "--tile", "2"],
                capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            info = json.loads(r.stdout)
            self.assertTrue((out / "audio16.wav").stat().st_size > 0)
            self.assertGreaterEqual(info["frames"], 2)
            self.assertGreaterEqual(info["sub_tiles"], 1)
            self.assertEqual(info["seconds_per_tile"], 2)
            self.assertEqual(info["sub_crop"], "320:29:0:178")


if __name__ == "__main__":
    unittest.main()
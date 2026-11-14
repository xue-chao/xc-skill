#!/usr/bin/env python3
"""Build a <=1MB base64-embedded HTML gallery from images (sips/ffmpeg compression)."""
import argparse
import base64
import html
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TEMPLATE = """<div style="font-family:-apple-system,'PingFang SC',sans-serif;background:#FBF6E3;color:#333;padding:16px;max-width:720px;margin:0 auto;">
<h2 style="text-align:center;margin:8px 0 12px;">{title}</h2>
{figures}
<style>figure{{margin:0 0 18px;}}img{{width:100%;border-radius:12px;display:block;}}figcaption{{font-size:13px;text-align:center;margin-top:6px;color:#6b5d3f;}}</style>
</div>"""


def compress(src, dst, width, quality):
    if shutil.which("sips"):
        subprocess.run(["sips", "-Z", str(width), "-s", "format", "jpeg",
                        "-s", "formatOptions", str(quality), str(src), "--out", str(dst)],
                       check=True, capture_output=True)
        return True
    if shutil.which("ffmpeg"):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
                        "-vf", f"scale={width}:-1", "-q:v", "6", str(dst)],
                       check=True, capture_output=True)
        return True
    return False


def jpeg_bytes(src, width, quality, no_compress):
    src = Path(src)
    if no_compress and src.suffix.lower() in (".jpg", ".jpeg"):
        return src.read_bytes()
    with tempfile.TemporaryDirectory() as td:
        dst = Path(td) / "out.jpg"
        if compress(src, dst, width, quality):
            return dst.read_bytes()
    return src.read_bytes()


def build(args):
    attempts = [(args.width, args.quality), (640, 25), (560, 15)]
    if args.no_compress:
        attempts = [(args.width, args.quality)]
    for width, quality in attempts:
        figures = []
        for img, cap in zip(args.img, args.cap):
            data = jpeg_bytes(img, width, quality, args.no_compress)
            b64 = base64.b64encode(data).decode()
            figures.append(
                f'<figure><img src="data:image/jpeg;base64,{b64}" alt="{html.escape(cap)}"/>'
                f"<figcaption>{html.escape(cap)}</figcaption></figure>")
        page = TEMPLATE.format(title=html.escape(args.title), figures="\n".join(figures))
        size = len(page.encode("utf-8"))
        if size <= args.max_bytes:
            Path(args.out).write_text(page)
            return size
    sys.exit(f"gallery exceeds {args.max_bytes} bytes even at lowest quality; use fewer images")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--max-bytes", type=int, default=1_000_000)
    ap.add_argument("--width", type=int, default=760)
    ap.add_argument("--quality", type=int, default=35)
    ap.add_argument("--no-compress", action="store_true")
    ap.add_argument("--img", action="append", required=True)
    ap.add_argument("--cap", action="append", required=True)
    args = ap.parse_args()
    if len(args.img) != len(args.cap):
        sys.exit("--img and --cap counts must match")
    size = build(args)
    print(f"wrote {args.out} ({size} bytes)")


if __name__ == "__main__":
    main()
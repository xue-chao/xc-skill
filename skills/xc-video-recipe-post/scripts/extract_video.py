#!/usr/bin/env python3
"""Extract 16kHz mono audio, keyframes and subtitle tiles from a video (ffmpeg)."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def video_size(video):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(video)],
        check=True, capture_output=True, text=True).stdout.strip()
    w, h = out.split("x")
    return int(w), int(h)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video")
    ap.add_argument("outdir")
    ap.add_argument("--frame-interval", type=float, default=2)
    ap.add_argument("--sub-fps", type=float, default=1)
    ap.add_argument("--tile", type=int, default=12)
    ap.add_argument("--sub-crop", help="W:H:X:Y override for the subtitle band")
    ap.add_argument("--no-subs", action="store_true")
    ap.add_argument("--no-frames", action="store_true")
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"missing {tool}; install e.g. brew install ffmpeg")

    out = Path(args.outdir)
    (out / "frames").mkdir(parents=True, exist_ok=True)
    (out / "subs").mkdir(parents=True, exist_ok=True)

    run(["ffmpeg", "-y", "-v", "error", "-i", args.video,
         "-vn", "-ac", "1", "-ar", "16000", str(out / "audio16.wav")])

    n_frames = 0
    if not args.no_frames:
        run(["ffmpeg", "-y", "-v", "error", "-i", args.video,
             "-vf", f"fps=1/{args.frame_interval:g}", "-q:v", "2",
             str(out / "frames" / "f_%03d.jpg")])
        n_frames = len(list((out / "frames").glob("f_*.jpg")))

    n_subs = 0
    crop = None
    if not args.no_subs:
        w, h = video_size(args.video)
        # default band: bottom ~12% of frame height, where vertical-video captions sit
        crop = args.sub_crop or f"{w}:{round(h * 0.12)}:0:{round(h * 0.74)}"
        run(["ffmpeg", "-y", "-v", "error", "-i", args.video,
             "-vf", f"fps={args.sub_fps:g},crop={crop},tile=1x{args.tile}",
             "-q:v", "2", str(out / "subs" / "m_%02d.jpg")])
        n_subs = len(list((out / "subs").glob("m_*.jpg")))

    print(json.dumps({
        "audio": str(out / "audio16.wav"),
        "frames": n_frames,
        "frame_interval_s": args.frame_interval,
        "sub_tiles": n_subs,
        "seconds_per_tile": args.tile / args.sub_fps,
        "sub_crop": crop,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
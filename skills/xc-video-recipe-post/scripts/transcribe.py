#!/usr/bin/env python3
"""Transcribe audio with whisper-cli; locate or download a suitable model."""
import argparse
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

MODELS = {
    "zh": ("ggml-large-v3-turbo.bin",
           "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin"),
    "en": ("ggml-small.en.bin",
           "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin"),
}


def resolve_model(lang, explicit):
    if explicit:
        return Path(explicit)
    env = os.environ.get("WHISPER_MODEL")
    if env:
        return Path(env)
    return Path.home() / "models" / MODELS.get(lang, MODELS["zh"])[0]


def download(url, dest, proxy):
    if not url.startswith("https://"):
        sys.exit("only HTTPS downloads allowed")
    handlers = []
    if proxy:
        handlers.append(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
    opener = urllib.request.build_opener(*handlers)
    req = urllib.request.Request(url, headers={"User-Agent": "xc-video-recipe-post"})
    with opener.open(req, timeout=60) as resp:
        ctype = resp.headers.get("Content-Type", "")
        if "html" in ctype:
            sys.exit(f"unexpected content-type: {ctype}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as f:
            shutil.copyfileobj(resp, f)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("audio")
    ap.add_argument("--out", required=True, help="output prefix for .txt/.srt")
    ap.add_argument("--lang", default="zh")
    ap.add_argument("--model")
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--download", action="store_true")
    ap.add_argument("--proxy")
    args = ap.parse_args()

    cli = shutil.which("whisper-cli")
    if not cli:
        sys.exit("missing whisper-cli; install e.g. brew install whisper-cpp")

    model = resolve_model(args.lang, args.model)
    if not model.exists():
        if not args.download:
            sys.exit(f"model not found: {model}; rerun with --download [--proxy URL]")
        url = MODELS.get(args.lang, MODELS["zh"])[1]
        print(f"downloading {url} -> {model}", file=sys.stderr)
        download(url, model, args.proxy)

    subprocess.run([cli, "-m", str(model), "-f", args.audio, "-l", args.lang,
                    "-t", str(args.threads), "-osrt", "-otxt", "-of", args.out],
                   check=True)
    print(f"{args.out}.txt\n{args.out}.srt")


if __name__ == "__main__":
    main()
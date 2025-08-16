#!/usr/bin/env python3
"""
Simple helper to download a model from the Hugging Face Hub.

Example:
  python scripts/download_model.py \
    --repo_id huseyincavus/gemma-3-270m-finance-merged \
    --cache_dir ./models

If the repo is private, pass --token YOUR_HF_TOKEN or set the HF_TOKEN env var.
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
from typing import Optional

from huggingface_hub import snapshot_download


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Download a model repo from Hugging Face Hub to a local cache dir")
    p.add_argument("--repo_id", default="huseyincavus/gemma-3-270m-finance-merged", help="Repo id on the Hub, e.g. owner/model-name")
    p.add_argument("--cache_dir", default="./models", help="Local directory to store the downloaded repo (cache_dir).")
    p.add_argument("--revision", default=None, help="Revision/branch/commit to download (optional)")
    p.add_argument("--token", default=None, help="Hugging Face token (optional). Can also be provided in HF_TOKEN env var")
    p.add_argument("--allow_patterns", nargs="*", default=None, help="Optional file glob patterns to restrict download, e.g. 'pytorch_model.bin' 'tokenizer.json'")
    p.add_argument("--force", action="store_true", help="Force re-download even if cached")
    p.add_argument("--print_export", action="store_true", help="Print an export command for LOCAL_MODEL_PATH env var")
    return p.parse_args()


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args() if argv is None else parse_args()

    repo_id = args.repo_id
    cache_dir = os.path.abspath(args.cache_dir)
    revision = args.revision
    token = args.token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN")
    allow_patterns = tuple(args.allow_patterns) if args.allow_patterns else None

    os.makedirs(cache_dir, exist_ok=True)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logging.info("Downloading repo '%s' to '%s'", repo_id, cache_dir)

    try:
        local_path = snapshot_download(
            repo_id=repo_id,
            revision=revision,
            cache_dir=cache_dir,
            token=token,
            allow_patterns=allow_patterns,
            force_download=args.force,
        )
    except Exception as e:
        logging.error("Failed to download repo: %s", e)
        return 2

    # Basic verification: check common model files exist
    expected = ["config.json", "tokenizer.json", "special_tokens_map.json"]
    found = {name: os.path.exists(os.path.join(local_path, name)) for name in expected}

    logging.info("Download finished. Local repo path: %s", local_path)
    logging.info("File checks: %s", ", ".join(f"%s=%s" % (k, v) for k, v in found.items()))

    if args.print_export:
        print(f"# To force local loading in the apps:\nexport LOCAL_MODEL_PATH='{local_path}'")

    # Print location for programmatic use
    print(local_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())

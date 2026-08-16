#!/usr/bin/env python
"""
Run a single RVC3/examples/*.py script under automated-test conditions.

Applies two kinds of test-only patching before executing the script's source:

  - matplotlib.pyplot.pause() is replaced with a no-op. It sleeps in real
    wall-clock time even under the headless Agg backend, which several
    examples (and the RTB PyPlot backend's own animation step) call in a
    loop -- left alone, a single script can take minutes to finish.
  - per-script literal source substitutions from examples_skiplist.yaml,
    e.g. capping a hardcoded animation loop count.

Never modifies the script on disk -- patches are applied to an in-memory
copy of its source before exec().

Usage:
    python tests/run_example.py RVC3/examples/walking.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

SKIPLIST_PATH = Path(__file__).resolve().parent / "examples_skiplist.yaml"


def load_config() -> dict:
    if not SKIPLIST_PATH.exists():
        return {}
    return yaml.safe_load(SKIPLIST_PATH.read_text()) or {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("script", type=Path)
    args = parser.parse_args()

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.pause = lambda *args, **kwargs: None

    config = load_config().get(args.script.name, {})
    source = args.script.read_text()
    for patch in config.get("patches", []):
        if patch["match"] not in source:
            print(
                f"warning: patch match {patch['match']!r} not found in {args.script.name}, skipping it",
                file=sys.stderr,
            )
            continue
        source = source.replace(patch["match"], patch["replace"])

    globals_ = {"__name__": "__main__", "__file__": str(args.script)}
    exec(compile(source, str(args.script), "exec"), globals_)
    return 0


if __name__ == "__main__":
    sys.exit(main())

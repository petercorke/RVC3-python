#!/usr/bin/env python
"""
Slow test: run every script in RVC3/examples/ and check it exits cleanly.

Each script runs in its own subprocess via run_example.py, which patches
away real-time sleeps (matplotlib.pyplot.pause) and applies any per-script
overrides in examples_skiplist.yaml (skip entirely, or cap a hardcoded
loop) before exec'ing the script's source. See run_example.py and
examples_skiplist.yaml for what's patched and why.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "RVC3" / "examples"
RUNNER = Path(__file__).resolve().parent / "run_example.py"
SKIPLIST_PATH = Path(__file__).resolve().parent / "examples_skiplist.yaml"


def _skiplist() -> dict:
    if not SKIPLIST_PATH.exists():
        return {}
    return yaml.safe_load(SKIPLIST_PATH.read_text()) or {}


def _scripts() -> list[Path]:
    return sorted(p for p in EXAMPLES_DIR.glob("*.py") if p.name != "__init__.py")


pytestmark = pytest.mark.slow


@pytest.mark.parametrize("script", _scripts(), ids=lambda p: p.name)
def test_example_runs(script: Path):
    skip = _skiplist().get(script.name, {})
    if skip.get("skip"):
        pytest.skip(skip.get("reason", "skiplisted"))

    result = subprocess.run(
        [sys.executable, str(RUNNER), str(script)],
        capture_output=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr.decode()[-3000:]

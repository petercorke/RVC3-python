#!/usr/bin/env python
"""
Slow test: run every figure generation script in figures/code/ and check it
exits cleanly.

The scripts are documentation of how the book's figures were made, so this is
a smoke test only: it checks that each script runs to completion under the
headless Agg backend, not that the figure looks right.  Each script runs in its
own subprocess, via run_example.py (which turns plt.pause() into a no-op), with
a throwaway working directory so the PDFs written by rvcprint do not land in
the repository.  Known failures are listed in figures_skiplist.yaml.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = REPO_ROOT / "figures" / "code"
RUNNER = Path(__file__).resolve().parent / "run_example.py"
SKIPLIST_PATH = Path(__file__).resolve().parent / "figures_skiplist.yaml"


def _skiplist() -> dict:
    if not SKIPLIST_PATH.exists():
        return {}
    return yaml.safe_load(SKIPLIST_PATH.read_text()) or {}


def _scripts() -> list[Path]:
    # only the fig*/box* scripts that generate book figures; skip OLD/ and any
    # scratch files (test*.py etc.) that happen to sit in the chapter folders
    found = []
    for pattern in ("fig*.py", "box_*.py"):
        found += FIGURES_DIR.glob(f"*/{pattern}")
    return sorted(p for p in found if p.name.count(" ") == 0)


pytestmark = pytest.mark.slow


@pytest.mark.parametrize("script", _scripts(), ids=lambda p: f"{p.parent.name}/{p.name}")
def test_figure_script_runs(script: Path):
    skip = _skiplist().get(f"{script.parent.name}/{script.name}", {})
    if skip.get("skip"):
        pytest.skip(skip.get("reason", "skiplisted"))

    with tempfile.TemporaryDirectory() as tmp:
        # some scripts save into this subfolder of the working directory
        (Path(tmp) / "Figures_generated").mkdir()
        result = subprocess.run(
            [sys.executable, str(RUNNER), str(script)],
            capture_output=True,
            timeout=180,
            cwd=tmp,
        )
    assert result.returncode == 0, result.stderr.decode()[-3000:]

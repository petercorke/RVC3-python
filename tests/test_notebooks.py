#!/usr/bin/env python
"""
Slow test: run the book's chapter notebooks via notebook_runner and check
each one for erroring cells.

Wraps notebook_runner.run_notebook() as one pytest case per notebook, so a
failure names the notebook directly instead of just "notebooks failed".
Warnings are tolerated (recorded in the report, not asserted against);
only actual cell errors or a load/kernel-level failure fail the test.
Still writes the same tests/reports/latest.md as running
notebook_runner.py directly.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import notebook_runner as nr

pytestmark = pytest.mark.slow

_results: list[nr.NotebookResult] = []


@pytest.mark.parametrize("notebook_name", nr.DEFAULT_NOTEBOOKS)
def test_notebook(notebook_name: str):
    path = nr.NOTEBOOKS_DIR / notebook_name
    if not path.exists():
        pytest.skip(f"{path} not found")

    skiplist = nr.load_skiplist().get(notebook_name, [])
    result = nr.run_notebook(path, skiplist, timeout=300)
    _results.append(result)

    assert result.load_error is None, result.load_error
    counts = result.counts()
    errors = [c for c in result.cells if c.status == "error"]
    detail = "; ".join(f"cell[{c.index}] {c.detail}" for c in errors)
    assert counts["error"] == 0, detail


def test_write_report():
    """Defined after test_notebook, so pytest's default source-order
    collection runs it last, once every notebook result is in."""
    if _results:
        nr.write_report(_results, Path(nr.REPORTS_DIR) / "latest.md")

#!/usr/bin/env python
"""
Execute the book's worked-example notebooks and report per-cell status.

Runs each notebook against the current kernel (whatever Python environment
this script itself is run with -- point it at RVC3_12's interpreter), and
classifies every code cell as one of:

    clean    -- ran, no error, no warning text in its output
    warning  -- ran, produced output matching /Warning|Deprecat/
    error    -- raised an exception
    skipped  -- matched an entry in skiplist.yaml, never executed

Never writes back to the source notebook -- runs against an in-memory copy,
so this is safe to run against the tracked notebooks at any time without
interacting with the nbstripout pre-commit hook or polluting real diffs.

Usage:
    python tests/notebook_runner.py                  # all notebooks/chap*.ipynb + app.ipynb
    python tests/notebook_runner.py notebooks/chap4.ipynb [more paths...]
    python tests/notebook_runner.py --timeout 600     # per-cell timeout in seconds (default 300)
"""

from __future__ import annotations

import argparse
import copy
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import nbformat
import yaml
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError, CellTimeoutError

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
SKIPLIST_PATH = Path(__file__).resolve().parent / "skiplist.yaml"
REPORTS_DIR = Path(__file__).resolve().parent / "reports"

WARNING_RE = re.compile(r"Warning|Deprecat", re.IGNORECASE)

DEFAULT_NOTEBOOKS = [f"chap{n}.ipynb" for n in range(2, 17)] + ["app.ipynb"]


@dataclass
class CellResult:
    index: int
    status: str  # clean | warning | error | skipped
    source_preview: str
    detail: str = ""  # skip reason, or error name+message, or warning text


@dataclass
class NotebookResult:
    name: str
    cells: list[CellResult] = field(default_factory=list)
    load_error: str | None = None

    def counts(self) -> dict[str, int]:
        c = {"clean": 0, "warning": 0, "error": 0, "skipped": 0}
        for cell in self.cells:
            c[cell.status] += 1
        return c


def load_skiplist() -> dict[str, list[dict[str, str]]]:
    if not SKIPLIST_PATH.exists():
        return {}
    with open(SKIPLIST_PATH) as f:
        return yaml.safe_load(f) or {}


def cell_source(cell) -> str:
    src = cell.get("source", "")
    return src if isinstance(src, str) else "".join(src)


def preview(text: str, n: int = 70) -> str:
    text = text.strip().replace("\n", " | ")
    return text if len(text) <= n else text[: n - 1] + "…"


def classify_outputs(outputs: list) -> tuple[str, str]:
    """Return (status, detail) for a cell that actually executed."""
    for out in outputs:
        if out.get("output_type") == "error":
            ename = out.get("ename", "")
            evalue = out.get("evalue", "")
            return "error", f"{ename}: {evalue}"

    warning_lines = []
    for out in outputs:
        # Only stderr carries real warnings.warn() output. Matching stdout
        # too causes false positives whenever printed data legitimately
        # contains the word "Warning" (e.g. OCR text extracted from an
        # image of a warning sign) -- that's cell output, not a warning.
        if out.get("output_type") == "stream" and out.get("name") == "stderr":
            text = out.get("text", "")
            text = text if isinstance(text, str) else "".join(text)
            for line in text.splitlines():
                if WARNING_RE.search(line):
                    warning_lines.append(line.strip())

    if warning_lines:
        return "warning", " / ".join(warning_lines[:3])

    return "clean", ""


def run_notebook(path: Path, skiplist: list[dict[str, str]], timeout: int) -> NotebookResult:
    result = NotebookResult(name=path.name)

    try:
        nb = nbformat.read(path, as_version=4)
    except Exception as e:  # noqa: BLE001
        result.load_error = f"{type(e).__name__}: {e}"
        return result

    nb = copy.deepcopy(nb)  # never touch the caller's notebook object

    skip_reason_by_index: dict[int, str] = {}
    for idx, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        src = cell_source(cell)
        for entry in skiplist:
            if entry["match"] in src:
                skip_reason_by_index[idx] = entry["reason"]
                cell["source"] = f"pass  # skipped by notebook_runner: {entry['reason']}"
                break

    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        allow_errors=True,
        resources={"metadata": {"path": str(path.parent)}},
    )

    try:
        client.execute()
    except (CellExecutionError, CellTimeoutError) as e:
        # allow_errors=True should prevent this for ordinary cell errors;
        # this path is for kernel-level failures (e.g. a hard timeout).
        result.load_error = f"kernel-level failure: {type(e).__name__}: {e}"
        return result

    for idx, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        if idx in skip_reason_by_index:
            result.cells.append(
                CellResult(idx, "skipped", preview(cell_source(cell)), skip_reason_by_index[idx])
            )
            continue
        status, detail = classify_outputs(cell.get("outputs", []))
        result.cells.append(CellResult(idx, status, preview(cell_source(cell)), detail))

    return result


def write_report(results: list[NotebookResult], out_path: Path) -> None:
    lines = ["# Notebook test run\n"]
    totals = {"clean": 0, "warning": 0, "error": 0, "skipped": 0}

    for r in results:
        counts = r.counts()
        for k, v in counts.items():
            totals[k] += v

        if r.load_error:
            lines.append(f"## {r.name} -- FAILED TO LOAD/RUN\n")
            lines.append(f"{r.load_error}\n")
            continue

        lines.append(
            f"## {r.name} -- {counts['clean']} clean, {counts['warning']} warning, "
            f"{counts['error']} error, {counts['skipped']} skipped\n"
        )
        for cell in r.cells:
            if cell.status == "clean":
                continue
            marker = {"warning": "WARN", "error": "FAIL", "skipped": "SKIP"}[cell.status]
            lines.append(f"- [{marker}] cell[{cell.index}] `{cell.source_preview}`")
            if cell.detail:
                lines.append(f"  {cell.detail}")
        lines.append("")

    lines.insert(
        1,
        f"**Totals:** {totals['clean']} clean, {totals['warning']} warning, "
        f"{totals['error']} error, {totals['skipped']} skipped\n",
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("notebooks", nargs="*", help="notebook paths (default: all core chapter notebooks)")
    parser.add_argument("--timeout", type=int, default=300, help="per-cell timeout in seconds (default 300)")
    parser.add_argument("--report", default=str(REPORTS_DIR / "latest.md"), help="output report path")
    args = parser.parse_args()

    os.environ.setdefault("MPLBACKEND", "Agg")  # never pop real GUI windows during an automated run

    if args.notebooks:
        paths = [Path(p) for p in args.notebooks]
    else:
        paths = [NOTEBOOKS_DIR / name for name in DEFAULT_NOTEBOOKS]

    skiplist_all = load_skiplist()

    results = []
    for path in paths:
        if not path.exists():
            print(f"-- {path}: SKIPPING, file not found", file=sys.stderr)
            continue
        print(f"-- running {path.name} ...", file=sys.stderr)
        skiplist = skiplist_all.get(path.name, [])
        results.append(run_notebook(path, skiplist, args.timeout))

    report_path = Path(args.report)
    write_report(results, report_path)
    print(f"report written to {report_path}", file=sys.stderr)

    total_errors = sum(r.counts()["error"] for r in results if not r.load_error)
    total_load_errors = sum(1 for r in results if r.load_error)
    return 1 if (total_errors or total_load_errors) else 0


if __name__ == "__main__":
    raise SystemExit(main())

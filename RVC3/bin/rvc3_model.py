#!/usr/bin/env python3
"""Run a bdsim model script (RVC3/models/<name>.py) directly from the shell.

Usage:
    rvc3-model <name> [args...]

Adds RVC3/models to sys.path first, matching how rvctool's %run -i/%run -m
already handle these scripts (some import sibling files, e.g. `from vloop
import vloop, B`), then runs the named script as if it were __main__ so its
`if __name__ == "__main__":` block executes.
"""

import sys
import runpy
from pathlib import Path

import RVC3.models as models


def main() -> None:
    models_dir = Path(models.__file__).parent

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        print("Available models:")
        for f in sorted(models_dir.glob("*.py")):
            if f.stem != "__init__":
                print(f"  {f.stem}")
        sys.exit(0)

    name = sys.argv[1]
    script = models_dir / f"{name}.py"
    if not script.exists():
        sys.exit(f"rvc3-model: no such model {name!r} (looked in {models_dir})")

    sys.path.insert(0, str(models_dir))
    sys.argv = [str(script)] + sys.argv[2:]
    runpy.run_path(str(script), run_name="__main__")


if __name__ == "__main__":
    main()

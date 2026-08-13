#!/usr/bin/env python
"""
Smoke tests for command-line entry points in RVC3.bin.

``--help`` verifies that imports and argument parsing work and the tool
exits cleanly. ``--test`` runs rvctool's own non-interactive environment
check and verifies its PASS/FAIL reporting and exit code.
"""

import subprocess
import sys
import unittest
from importlib.metadata import PackageNotFoundError, version

try:
    version("open3d")
    _open3d_available = True
except PackageNotFoundError:
    _open3d_available = False


def _run(args: list[str], timeout: float | None = None) -> subprocess.CompletedProcess:
    """Run a command via the current Python interpreter's entry-point module."""
    return subprocess.run(
        [sys.executable, "-m"] + args,
        capture_output=True,
        timeout=timeout,
    )


class TestRvctool(unittest.TestCase):

    def test_help(self):
        result = _run(["RVC3.bin.rvctool", "--help"])
        self.assertEqual(result.returncode, 0, msg=result.stderr.decode())

    def test_smoke_test(self):
        """--test always exercises RTB, MVTB, SG, SMTB and bdsim; Open3D's
        result depends on whether it's installed in this environment, but
        either way it must be reported explicitly, not silently skipped."""
        result = _run(["RVC3.bin.rvctool", "--test"], timeout=60)
        stdout = result.stdout.decode()
        self.assertIn("[PASS] RTB: Panda().fkine()", stdout, msg=stdout)
        self.assertIn("[PASS] MVTB: Image.Read + smooth()", stdout, msg=stdout)
        self.assertIn("[PASS] SG: Cuboid()", stdout, msg=stdout)
        self.assertIn("[PASS] SMTB: SE3 composition", stdout, msg=stdout)
        self.assertIn("[PASS] bdsim: vloop_test block diagram run", stdout, msg=stdout)
        if _open3d_available:
            self.assertIn("[PASS] Open3D: PointCloud creation", stdout, msg=stdout)
            self.assertEqual(result.returncode, 0, msg=stdout)
        else:
            self.assertIn("Open3D: point cloud support: not installed", stdout, msg=stdout)
            self.assertEqual(result.returncode, 1, msg=stdout)


if __name__ == "__main__":
    unittest.main()

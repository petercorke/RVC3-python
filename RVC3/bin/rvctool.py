#!/usr/bin/env python3
"""
Interactive Robotics, Vision & Control shell -- starts an IPython session
with NumPy, RTB, MVTB, SG and SpatialMath pre-imported.

Usage::

    $ rvctool
    $ rvctool myscript.py
"""

# import stuff
import argparse
import os
import shlex
import sys
import textwrap
from importlib.metadata import PackageNotFoundError, version
from math import pi  # lgtm [py/unused-import]
import pathlib

import matplotlib as mpl

# imports for use by IPython and user
import numpy as np
from scipy import linalg, optimize
import matplotlib.pyplot as plt  # lgtm [py/unused-import]
from spatialmath import *  # lgtm [py/polluting-import]
from spatialmath.base import *
from spatialmath.base import sym

from RVC3.bin import _bintools

try:
    from colored import fg, bg, attr

    _colored = True
    # print('using colored output')
except ImportError:
    # print('colored not found')
    _colored = False
    fg = lambda *args, **kwargs: ""
    bg = lambda *args, **kwargs: ""
    attr = lambda *args, **kwargs: ""

_OPTIONS_ENVVAR = "RVCTOOL_OPTIONS"
_LEGACY_OPTIONS_ENVVAR = "RVCTOOL"


def env_arguments(parser):
    """Return command-line style options from the environment.

    Prefers :data:`_OPTIONS_ENVVAR`; falls back to the deprecated
    :data:`_LEGACY_OPTIONS_ENVVAR` (printing a one-line warning) if the
    new variable isn't set.

    :param parser: argument parser used for error reporting
    :type parser: :class:`argparse.ArgumentParser`
    :return: tokenised environment arguments
    :rtype: list[str]
    """
    options = os.environ.get(_OPTIONS_ENVVAR)
    if options is None:
        options = os.environ.get(_LEGACY_OPTIONS_ENVVAR)
        if options is not None:
            print(
                f"Warning: the {_LEGACY_OPTIONS_ENVVAR} environment variable is "
                f"deprecated, use {_OPTIONS_ENVVAR} instead",
                file=sys.stderr,
            )

    if not options:
        return []

    try:
        return shlex.split(options)
    except ValueError as exc:
        parser.error(f"invalid {_OPTIONS_ENVVAR}: {exc}")


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="rvctool",
        formatter_class=_bintools.LineWrapRawTextDefaultsHelpFormatter,
        epilog=(
            "options can be set via the environment variable RVCTOOL_OPTIONS "
            "(or the deprecated RVCTOOL), for example:\n\n"
            "    $ export RVCTOOL_OPTIONS=\"--backend TkAgg --prompt 'rvc> ' "
            '--reload"\n'
        ),
        description=(
            "Interactive python enviroment for exploring the Robotics & Machine Vision"
            " toolboxes for Python"
        ),
    )
    parser.add_argument("script", default=None, nargs="?", help="specify script to run")

    parser.add_argument(
        "-B", "--backend", default=None, help="specify graphics backend"
    )
    parser.add_argument(
        "-C",
        "--color",
        default="neutral",
        help=(
            "specify terminal color scheme (neutral, lightbg, nocolor, linux), linux is"
            " for dark mode"
        ),
    )
    parser.add_argument(
        "--confirmexit", "-x", default=False, action="store_true", help="confirm exit"
    )
    parser.add_argument("--prompt", "-p", default="RVC3 >>> ", help="input prompt")
    parser.add_argument(
        "-r",
        "--resultprefix",
        default=None,
        help="execution result prefix, include {} for execution count number",
    )
    parser.add_argument(
        "-b",
        "--no-banner",
        dest="banner",
        default=True,
        action="store_false",
        help="suppress startup banner",
    )
    parser.add_argument(
        "-c",
        "--nocwd",
        dest="cwd",
        default=True,
        action="store_false",
        help="suppress cwd to RVC3 folder",
    )
    parser.add_argument(
        "-a",
        "--showassign",
        default=True,
        action="store_true",
        help="display the result of assignments",
    )
    parser.add_argument(
        "--book",
        default=False,
        action=argparse.BooleanOptionalAction,
        help=(
            "match the book's printed transcripts exactly: plain '>>> ' prompt, "
            "no Out[N]: labels, no ANSI matrix colouring"
        ),
    )
    parser.add_argument(
        "-R",
        "--no-robot",
        dest="robot",
        default=True,
        action="store_false",
        help="do not import robotics toolbox (RTB-P)",
    )
    parser.add_argument(
        "-V",
        "--no-vision",
        dest="vision",
        default=True,
        action="store_false",
        help="do not import vision toolbox (MVTB-P)",
    )
    parser.add_argument(
        "--ansi",
        default=True,
        action=argparse.BooleanOptionalAction,
        help=(
            "use ANSImatrix to display matrices -- colour codes can be problematic "
            "when copying/pasting terminal output, pass --no-ansi to disable"
        ),
    )
    parser.add_argument(
        "-e",
        "--examples",
        default=True,
        action="store_true",
        help="change working directory to shipped examples",
    )
    parser.add_argument(
        "-s",
        "--swift",
        default=False,
        action="store_true",
        help="use Swift as default backend",
    )
    parser.add_argument(
        "--torch",
        default=False,
        action="store_true",
        help="import torch and torchvision if installed",
    )
    parser.add_argument(
        "--reload",
        default=False,
        action="store_true",
        help="enable autoreload of any imported modules, same as IPython's builtin %%autoreload 2",
    )
    parser.add_argument(
        "--test",
        default=False,
        action="store_true",
        help="non-interactive environment smoke test: print package versions, "
        "exercise one real code path per toolbox (RTB, MVTB, SG, SMTB, bdsim, "
        "Open3D), exit 0/1 instead of starting an interactive shell",
    )

    argv = env_arguments(parser) + sys.argv[1:]
    args, rest = parser.parse_known_args(argv)

    if args.script is not None:
        args.banner = False

    return args, rest


def optional_torch_imports(enable):
    """Optionally import torch and torchvision.

    :param enable: if ``True``, attempt optional imports
    :type enable: bool
    :return: tuple of imported modules dictionary and warning messages
    :rtype: tuple(dict, list)
    """
    modules = {}
    warnings = []

    if not enable:
        return modules, warnings

    try:
        import torch as _torch

        modules["torch"] = _torch
    except ImportError:
        warnings.append("PyTorch (torch) not found")

    try:
        import torchvision as _torchvision

        modules["torchvision"] = _torchvision
    except ImportError:
        warnings.append("TorchVision (torchvision) not found")

    return modules, warnings


def get_versions(args, torch_modules=None):
    """Package version strings shown in the banner and by --test.

    :param args: parsed command-line arguments
    :param torch_modules: optional imported torch/torchvision modules
    :type torch_modules: dict, optional
    :return: version strings, one per package
    :rtype: list[str]
    """
    torch_modules = torch_modules or {}

    versions = [f"Python=={sys.version.split()[0]}"]
    if args.robot:
        versions.append(f"RTB=={version('roboticstoolbox-python')}")
    if args.vision:
        versions.append(f"MVTB=={version('machinevision-toolbox-python')}")
    versions.append(f"SG=={version('spatialgeometry')}")
    versions.append(f"SMTB=={version('spatialmath-python')}")
    versions.append(f"bdsim=={version('bdsim')}")
    versions.append(f"NumPy=={version('numpy')}")
    versions.append(f"SciPy=={version('scipy')}")
    versions.append(f"Matplotlib=={version('matplotlib')}")
    try:
        versions.append(f"Open3D=={version('open3d')}")
    except PackageNotFoundError:
        versions.append("Open3D==not installed")
    if "torch" in torch_modules:
        versions.append(
            f"PyTorch=={getattr(torch_modules['torch'], '__version__', 'unknown')}"
        )
    if "torchvision" in torch_modules:
        versions.append(
            "TorchVision=="
            f"{getattr(torch_modules['torchvision'], '__version__', 'unknown')}"
        )
    return versions


def make_banner(args, torch_modules=None):
    # http://patorjk.com/software/taag/#p=display&f=Standard&t=RVC%203
    # print the banner: standard
    # https://patorjk.com/software/taag/#p=display&f=Standard&t=Robotics%2C%20Vision%20%26%20Control%203

    banner = fg("yellow")
    banner += r""" ____       _           _   _             __     ___     _                ___      ____            _             _   _____
|  _ \ ___ | |__   ___ | |_(_) ___ ___    \ \   / (_)___(_) ___  _ __    ( _ )    / ___|___  _ __ | |_ _ __ ___ | | |___ /
| |_) / _ \| '_ \ / _ \| __| |/ __/ __|    \ \ / /| / __| |/ _ \| '_ \   / _ \/\ | |   / _ \| '_ \| __| '__/ _ \| |   |_ \
|  _ < (_) | |_) | (_) | |_| | (__\__ \_    \ V / | \__ \ | (_) | | | | | (_>  < | |__| (_) | | | | |_| | | (_) | |  ___) |
|_| \_\___/|_.__/ \___/ \__|_|\___|___( )    \_/  |_|___/_|\___/|_| |_|  \___/\/  \____\___/|_| |_|\__|_|  \___/|_| |____/
                                          |/
for Python

"""

    versions = "You're running: " + ", ".join(get_versions(args, torch_modules))
    banner += "\n".join(
        textwrap.wrap(
            versions,
            break_long_words=False,
            subsequent_indent=" " * len("You're running: "),
            width=80,
        )
    )

    banner += r"""

    import math
    import numpy as np
    from scipy import linalg, optimize
    import matplotlib.pyplot as plt
    from spatialmath import *
    from spatialmath.base import *
    from spatialmath.base import sym
    """
    if args.robot:
        banner += """from spatialgeometry import *
    from roboticstoolbox import *
    """
    if args.vision:
        banner += """from machinevisiontoolbox import *
    import machinevisiontoolbox.base as mvb
    """

    banner += r"""
    # useful variables
    from math import pi
    puma = models.DH.Puma560()
    panda = models.DH.Panda()

    func/object?       - show brief help
    help(func/object)  - show detailed help
    func/object??      - show source code
    """
    banner += attr(0)

    return banner


def run_smoke_test(args) -> bool:
    """Non-interactive environment sanity check, used by --test.

    Not a substitute for the pytest suite -- a fast, human- or script-run
    "did this environment actually come together correctly" check: real
    versions, and one real result per toolbox, checked against a sanity
    condition rather than just "it didn't raise". Missing optional
    dependencies (e.g. Open3D) are reported as a FAIL with the reason, not
    silently skipped.

    :param args: parsed command-line arguments
    :return: ``True`` if every check passed
    :rtype: bool
    """
    # force a non-interactive backend so this never pops a GUI window
    mpl.use("Agg", force=True)

    print(", ".join(get_versions(args)))

    checks: list[tuple[str, bool]] = []

    try:
        from roboticstoolbox import models

        panda = models.DH.Panda()
        T = panda.fkine(panda.qz)
        ok = T.shape == (4, 4) and np.isclose(np.linalg.det(T.R), 1.0)
        checks.append(("RTB: Panda().fkine() (kinematics)", ok))
    except Exception as e:
        checks.append((f"RTB: Panda().fkine() (kinematics): {e}", False))

    try:
        from machinevisiontoolbox import Image

        img = Image.Read("monalisa.png", mono=True)
        smoothed = img.smooth(sigma=2)
        ok = smoothed.shape == img.shape and not np.array_equal(
            smoothed.array, img.array
        )
        checks.append(("MVTB: Image.Read + smooth() (OpenCV-backed)", ok))
    except Exception as e:
        checks.append((f"MVTB: Image.Read + smooth() (OpenCV-backed): {e}", False))

    try:
        from spatialgeometry import Cuboid

        cube = Cuboid(scale=[1, 1, 1])
        ok = list(cube.scale) == [1, 1, 1]
        checks.append(("SG: Cuboid() (shape creation)", ok))
    except Exception as e:
        checks.append((f"SG: Cuboid() (shape creation): {e}", False))

    try:
        T = SE3.Rx(pi / 2) * SE3.Rx(-pi / 2)
        ok = np.allclose(T.A, np.eye(4), atol=1e-9)
        checks.append(("SMTB: SE3 composition (identity check)", ok))
    except Exception as e:
        checks.append((f"SMTB: SE3 composition (identity check): {e}", False))

    try:
        import open3d  # noqa: F401  -- presence check
    except ImportError as e:
        checks.append((f"Open3D: point cloud support: not installed ({e})", False))
    else:
        try:
            import open3d as o3d

            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(np.random.rand(10, 3))
            checks.append(("Open3D: PointCloud creation", len(pcd.points) == 10))
        except Exception as e:
            checks.append((f"Open3D: PointCloud creation: {e}", False))

    try:
        import importlib

        import RVC3

        models_dir = pathlib.Path(RVC3.__path__[0]) / "models"
        if str(models_dir) not in sys.path:
            sys.path.insert(0, str(models_dir))
        # bdsim's own BDSim()/run() read sys.argv for their own flags (-g, -H,
        # ...), both at BDSim() construction (module import time here) and at
        # run() -- clear it for both so rvctool's own arguments aren't
        # misread as bdsim's.
        saved_argv, sys.argv = sys.argv, sys.argv[:1]
        try:
            vloop_test = importlib.import_module("vloop_test")
            # both are read dynamically at run() time, not baked in at
            # construction, so overriding them post-import is safe
            vloop_test.sim.options.quiet = True
            vloop_test.sim.options.graphics = False
            out = vloop_test.sim.run(vloop_test.bd, 0.1, dt=1e-3)
        finally:
            sys.argv = saved_argv
        ok = np.isclose(out.t[-1], 0.1) and out.x.shape[0] > 0
        checks.append(("bdsim: vloop_test block diagram run", ok))
    except Exception as e:
        checks.append((f"bdsim: vloop_test block diagram run: {e}", False))

    for name, passed in checks:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")

    n_passed = sum(1 for _, passed in checks if passed)
    print(f"rvctool --test: {n_passed}/{len(checks)} checks passed")
    return n_passed == len(checks)


def startup():
    plt.ion()


def main():
    args, ipython_args = parse_arguments()

    if args.test:
        sys.exit(0 if run_smoke_test(args) else 1)

    try:
        import IPython
        from IPython.terminal.prompts import Prompts
        from pygments.token import Token
        from traitlets.config import Config
    except ImportError as e:
        sys.exit(
            f"rvctool requires IPython and pygments, which are not "
            f"installed ({e}).\nInstall them with:\n\n"
            "    pip install rvc3python[tool]\n"
        )

    if args.book:
        # match the book's printed transcripts exactly
        args.resultprefix = ""
        args.prompt = ">>> "
        args.ansi = False

    # setup defaults
    np.set_printoptions(
        linewidth=120,
        formatter={"float": lambda x: f"{x:8.4g}" if abs(x) > 1e-10 else f"{0:8.4g}"},
    )

    torch_modules, torch_warnings = optional_torch_imports(args.torch)

    globs = globals()
    if args.robot:
        exec("from spatialgeometry import *", globs)
        exec("from roboticstoolbox import *", globs)
        from roboticstoolbox import __path__

        sys.path.append(str(pathlib.Path(__path__[0]) / "examples"))

        # load some robot models
        globs["puma"] = models.DH.Puma560()
        globs["panda"] = models.DH.Panda()

        # set default backend for Robot.plot
        if args.swift:
            Robot.default_backend = "swift"

    if args.vision:
        exec("from machinevisiontoolbox import *", globs)
        exec("import machinevisiontoolbox.base as mvb", globs)

    globs.update(torch_modules)

    # set matrix printing mode for spatialmath
    SE3._ansimatrix = args.ansi

    # set default matplotlib backend
    if args.backend is not None:
        print(f"Using matplotlib backend {args.backend}")
        mpl.use(args.backend)

    if args.banner:
        banner = make_banner(args, torch_modules)
        print(banner)

    for warning in torch_warnings:
        print(f"Warning: {warning}")

    if args.showassign and args.banner:
        print(
            fg("red")
            + "Results of assignments will be displayed, use trailing ; to suppress"
            + attr(0)
            + "\n"
        )

    # append to the module path
    # - RVC3 models and examples
    # - RTB examples
    root = pathlib.Path(__file__).absolute().parent.parent
    sys.path.append(str(root / "models"))
    sys.path.append(str(root / "examples"))

    if args.cwd:
        os.chdir(root)

    class MyPrompt(Prompts):
        def in_prompt_tokens(self, cli=None):
            # args.prompt always has a real value now (default "RVC3 >>> "),
            # so this is never falling back to IPython's native In[N]: prompt.
            return [(Token.Prompt, args.prompt)]

        def out_prompt_tokens(self, cli=None):
            if args.resultprefix is None:
                # traditional behaviour
                return super().out_prompt_tokens()
            else:
                return [
                    (Token.Prompt, args.resultprefix.format(self.shell.execution_count))
                ]

    # set configuration options, there are lots, see
    # https://ipython.readthedocs.io/en/stable/config/options/terminal.html
    c = Config()
    c.InteractiveShellEmbed.colors = args.color
    c.InteractiveShell.confirm_exit = args.confirmexit
    c.InteractiveShell.prompts_class = MyPrompt
    if args.showassign:
        c.InteractiveShell.ast_node_interactivity = "last_expr_or_assign"
    # rvctool prints its own banner above (when args.banner is set); IPython's
    # own generic banner would just be redundant noise stacked underneath it
    c.TerminalIPythonApp.display_banner = False

    # set precision, same as %precision
    c.PlainTextFormatter.float_precision = "%.3f"

    # set up a script to be executed by IPython when we get there
    code = None
    if args.script is not None:
        path = pathlib.Path(args.script)
        if not path.exists():
            raise ValueError(f"script does not exist: {args.script}")
        code = path.open("r").readlines()

    if code is None:
        code = [
            "startup()",
            "_prec = get_ipython().run_line_magic('precision', '%.3g'); "
            "print(f'Default numeric formatting: {_prec}')",
        ]

    if args.reload:
        code = ["%load_ext autoreload", "%autoreload 2"] + code

    c.InteractiveShellApp.exec_lines = code

    # clear argv so IPython doesn't try to reparse arguments we've already consumed
    sys.argv = sys.argv[:1]
    IPython.start_ipython(config=c, user_ns=globs, argv=ipython_args)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

# a simple Robotics & Vision Toolbox "shell", runs Python3 and loads
# NumPy, SciPy, RTB-P, SMTB-P, MVTB-P.
#
# Run it from the shell
#  $ rvctool
#
# Default switches can be set using the environent variables RVCTOOL, eg.
#
#  setenv RVCTOOL "-n"
#  export RVCTOOL="-n"

# import stuff
import os
from pathlib import Path
import sys
from importlib.metadata import version
import argparse

from pygments.token import Token
from IPython.terminal.prompts import Prompts
from IPython.terminal.prompts import ClassicPrompts
from traitlets.config import Config
import IPython
import matplotlib as mpl

try:
    from colored import fg, bg, attr

    _colored = True
    # print('using colored output')
except ImportError:
    # print('colored not found')
    _colored = False

# imports for use by IPython and user
from math import pi  # lgtm [py/unused-import]
import numpy as np
from scipy import linalg, optimize
import matplotlib.pyplot as plt  # lgtm [py/unused-import]
from spatialmath import *  # lgtm [py/polluting-import]
from spatialmath.base import *
from spatialmath.base import sym


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="rvctool",
        epilog=(
            "To set defaults put the relevant command line switches as a string in the"
            " environment varible RVCTOOL."
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
    parser.add_argument("--confirmexit", "-x", default=False, help="confirm exit")
    parser.add_argument("--prompt", "-p", default=None, help="input prompt")
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
        default=False,
        action="store_true",
        help="do not display the result of assignments",
    )
    parser.add_argument(
        "-n",
        "--normal",
        dest="book",
        default=True,
        action="store_false",
        help="use normal ipython settings for prompts and display on assignment",
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
        default=False,
        action="store_true",
        help="use ANSImatrix to display matrices",
    )
    parser.add_argument(
        "-e",
        "--examples",
        default=False,
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

    # add options for light/dark mode

    env = os.getenv("RVCTOOL")
    if env is not None:
        # if envariable is set, parse it just like command line options
        args = parser.parse_args(env.split())
        # then use it to set the defaults for the actual command line parsing
        parser.set_defaults(**args.__dict__)

    args, rest = parser.parse_known_args()

    # remove the arguments we've just parsed from sys.argv so that IPython can have a
    # go at them later
    sys.argv = [sys.argv[0]] + rest

    if args.script is not None:
        args.banner = False

    return args


def make_banner(args):
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
for Python"""

    versions = []
    if args.robot:
        versions.append(f"RTB=={version('roboticstoolbox-python')}")
    if args.vision:
        versions.append(f"MVTB=={version('machinevision-toolbox-python')}")
    try:
        versions.append(f"SG=={version('spatialmath-python')}")
    except:
        pass
    versions.append(f"SMTB=={version('spatialmath-python')}")
    versions.append(f"NumPy=={version('numpy')}")
    versions.append(f"SciPy=={version('scipy')}")
    versions.append(f"Matplotlib=={version('matplotlib')}")

    # create banner
    banner += " (" + ", ".join(versions) + ")"
    banner += r"""

    import math
    import numpy as np
    from scipy import linalg, optimize
    import matplotlib.pyplot as plt
    from spatialmath import *
    from spatialmath.base import *
    from spatialmath.base import sym
    from spatialgeometry import *
    """
    if args.robot:
        banner += "from roboticstoolbox import *\n"
    if args.vision:
        banner += """    from machinevisiontoolbox import *
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


def startup():
    plt.ion()


def main():
    args = parse_arguments()
    # print(args)

    if args.book:
        # set book options
        args.resultprefix = ""
        args.prompt = ">>> "
        args.showassign = True
        args.ansi = False
        args.examples = True

    # setup defaults
    np.set_printoptions(
        linewidth=120,
        formatter={"float": lambda x: f"{x:8.4g}" if abs(x) > 1e-10 else f"{0:8.4g}"},
    )

    globs = globals()
    if args.robot:
        exec("from spatialgeometry import *", globs)
        exec("from roboticstoolbox import *", globs)
        from roboticstoolbox import __path__

        sys.path.append(str(Path(__path__[0]) / "examples"))

        # load some robot models
        globs["puma"] = models.DH.Puma560()
        globs["panda"] = models.DH.Panda()

        # set default backend for Robot.plot
        if args.swift:
            Robot.default_backend = "swift"

    if args.vision:
        exec("from machinevisiontoolbox import *", globs)
        exec("import machinevisiontoolbox.base as mvbase", globs)

    # set matrix printing mode for spatialmath
    SE3._ansimatrix = args.ansi

    # set default matplotlib backend
    if args.backend is not None:
        print(f"Using matplotlib backend {args.backend}")
        mpl.use(args.backend)

    if args.banner:
        banner = make_banner(args)
        print(banner)

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
    root = Path(__file__).absolute().parent.parent
    sys.path.append(str(root / "models"))
    sys.path.append(str(root / "examples"))

    if args.cwd:
        os.chdir(root)

    class MyPrompt(Prompts):
        def in_prompt_tokens(self, cli=None):
            if args.prompt is None:
                return super().in_prompt_tokens()
            else:
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
    # c.InteractiveShell.prompts_class = ClassicPrompts
    c.InteractiveShell.prompts_class = MyPrompt
    if args.showassign:
        c.InteractiveShell.ast_node_interactivity = "last_expr_or_assign"
    c.TerminalIPythonApp.display_banner = args.banner

    # set precision, same as %precision
    c.PlainTextFormatter.float_precision = "%.3f"

    # set up a script to be executed by IPython when we get there
    code = None
    if args.script is not None:
        path = Path(args.script)
        if not path.exists():
            raise ValueError(f"script does not exist: {args.script}")
        code = path.open("r").readlines()

    if code is None:
        code = [
            "startup()",
            "%precision %.3g;",
        ]

    c.InteractiveShellApp.exec_lines = code
    IPython.start_ipython(config=c, user_ns=globals())


if __name__ == "__main__":
    main()

# helper functions for creating figures for RVC3 Python book

import sys
import os
import os.path
import subprocess
import inspect
from collections.abc import Iterable
import re
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib import colors

fileparts = re.compile(r'fig(?P<chapter>[0-9]+|[A-K])_(?P<fig>.+).py')

def bdmodel(model, subfig=''):
    """Print bdsim model to a file

    :param model: name of the bdsim model file, including ``.bd`` extension
    :type model: str
    :param subfig: subfigure designation, typically a single lower, defaults to ''
    :type subfig: str, optional

    Invokes ``bdedit`` to render the model as a PDF file.
    """
    file = outfile(format='pdf', subfig=subfig)
    os.system(f"bdedit -s=14 ../../models/{model} -p {str(file)}")

def outfile(subfig='', format=None, include=False):
    """Generate name of output file

    :param subfig: subfigure designation, typically a single lower, defaults to ''
    :type subfig: str, optional
    :param format: file format, defaults to 'pdf'
    :type format: str, optional
    :param include: add "-include" to the generated path, defaults to False
    :type include: bool, optional
    :return: path where figure is to be stored
    :rtype: Path

    The path is derived from the name of
    the script that invokes ``rvcprint``, for example, calling ``outfile`` from
    the file ``fig6_1.py`` will return ``fig6_1.pdf``.

    The option ``include`` changes the path to ``fig6_1-include.pdf`` and would
    be used to create a PDF that is subsequently edited to form the included
    figure ``fig6_1.pdf``.  This prevents accidental overwriting of a hand
    edited figure.
    """
    # build the path for saving
    try:
        m = fileparts.search(os.path.basename(sys.argv[0]))
        chapter = m.group('chapter')
        fig = m.group('fig')
    except:
        print('bad file name')

    # change this next line to set figure output location
    path = Path(".")

    if include:
        figure = path / f"fig{chapter}_{fig}{subfig}-include.{format}"
    else:
        figure = path / f"fig{chapter}_{fig}{subfig}.{format}"

    print('saving --> ', figure)

    return figure

def figname(subfig=''):
    return os.path.splitext(os.path.basename(sys.argv[0]))[0]

def rvcprint(subfig='', thicken=1.5, facecolor='white', interval=None, ax=None, fignum=None, format='pdf', pause=2, debug=False, **kwargs):
    """Save Matplotlib figure as a PDF file

    :param subfig: subfigure designation, typically a single lower, defaults to ''
    :type subfig: str, optional
    :param thicken: set all lines this ``linewidth``, set to ``None`` to disable, defaults to 1.5
    :type thicken: float, optional
    :param facecolor: background color of the plot, defaults to 'white'
    :type facecolor: str, optional
    :param interval: specify tick interval, defaults to Matplotlib default
    :type interval: float, 2-tuple, 3-tuple, optional
    :param ax: use these axes instead of current figure, defaults to None
    :type ax: Axes, optional
    :param fignum: use this figure number instead of current figure, defaults to None
    :type fignum: int, optional
    :param format: file format, defaults to 'pdf'
    :type format: str, optional
    :param pause: delay time in seconds when the tweaked figure is displayed, defaults to 2
    :type pause: float, optional
    :param debug: block after figure has been tweaked but before saving, defaults to False
    :type debug: bool, optional

    The figure is saved as a PDF file with the root name equal to the name of
    the script that invokes ``rvcprint``, for example, calling ``rvcprint`` from
    the file ``fig6_1.py`` will save the figure as ``fig6_1.pdf``.

    Lines are thickened, axis labels are bolded.  
    
    Tick interval is adjusted by ``interval``
    - float, set this interval for all axes
    - 2-tuple, set intervals for x- and y-axes
    - 3-tupe, set intervals for x-, y- and z-axes

    :seealso: :func:`outfile`
    """
    # if the envariable RVCPRINT is 'no' then don't save the figure
    # this can be set by runall.py
    if os.getenv('RVCPRINT') == 'no':
        return

    figure = outfile(subfig=subfig, format=format)

    fontsize = 9

    if fignum is not None:
        plt.figure(fignum)

    if ax is None:
        axes = plt.gcf().get_axes()
    else:
        axes = [ax]

    for ax in axes:

        # bolden the axis labels
        a = ax.xaxis.get_label()
        a.set_fontweight('bold')
        ax.set_xlabel(a.get_text())

        a = ax.yaxis.get_label()
        a.set_fontweight('bold')
        ax.set_ylabel(a.get_text())

        if thicken is not None:
            for line in ax.get_lines():
                if line.get_linewidth() > 0:
                    line.set_linewidth(thicken)

            # thicken lines in legend
            legend = ax.get_legend()
            if legend is not None:
                for legobj in legend.legendHandles:
                    legobj.set_linewidth(thicken)
                # ax.legend(prop=dict(size=18))
                # legend.set_fontsize(20)
                plt.setp(legend.get_texts(), fontsize=fontsize)

        # ax.set_xticks(fontsize=fontsize)
        # ax.set_yticks(fontsize=fontsize)
        ax.tick_params(axis='both', which='major', labelsize=fontsize)

        try:
            ax.zaxis.set_tick_params(labelsize=fontsize)
        except AttributeError:
            pass

        if interval is not None:
            if not isinstance(interval, Iterable):
                interval = (interval,) * 3
            for i in range(3):
                if interval[0] is not None:
                    ax.xaxis.set_major_locator(MultipleLocator(interval[0]))
                if interval[1] is not None:
                    ax.yaxis.set_major_locator(MultipleLocator(interval[1]))

                try:
                    if interval[2] is not None:
                        ax.zaxis.set_major_locator(MultipleLocator(interval[2]))
                except:
                    pass

        dims = 2
        try:
            a = ax.zaxis.get_label()
            a.set_fontweight('bold')
            ax.set_zlabel(a.get_text())
            dims = 3
        except BaseException:
            pass

    if debug:
        plt.show(block=True)
    else:
        # save it

        for ax in axes:

            if facecolor is not None:
                if dims == 3:
                    rgba = colors.to_rgba(facecolor)
                    ax.w_xaxis.set_pane_color(rgba)
                    ax.w_yaxis.set_pane_color(rgba)
                    ax.w_zaxis.set_pane_color(rgba)

                ax.set_facecolor(facecolor)

            # get legend
            legend = ax.get_legend()
            if legend is not None and facecolor is not None:
                frame = legend.get_frame()
                frame.set_facecolor(facecolor)
                frame.set_edgecolor('black')


        plt.savefig(figure, format=format, facecolor=facecolor)

        if format == 'pdf':
            # crop it
            try:
                subprocess.run(['pdfcrop', figure, figure], capture_output=True)
            except FileNotFoundError:
                print('pdfcrop not found, not cropping')

        if pause > 0:
            plt.pause(pause)

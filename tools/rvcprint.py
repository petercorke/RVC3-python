import sys
import os
import os.path
import matplotlib.pyplot as plt
from collections.abc import Iterable
from matplotlib.ticker import MultipleLocator
import re
from pathlib import Path

fileparts = re.compile(r'fig(?P<chapter>[0-9]+)_(?P<fig>[0-9]+).py')

def outfile(subfig='', format=None):
    # build the path for saving
    try:
        m = fileparts.search(os.path.basename(sys.argv[0]))
        chapter = m.group('chapter')
        fig = m.group('fig')
    except:
        print('bad file name')

    # figure = os.path.splitext(figure)[0] + subfig + '.' + format
    # chapter = figure[3]

    path = Path(f"/Users/corkep/code/RVC3-python/chapter{chapter}"
        f"/Figures_generated")
    
    if not path.exists():
        print('creating folder', path)
        path.mkdir()

    figure = path / f"fig{chapter}_{fig}{subfig}.{format}"
    return figure

def rvcprint(subfig='', thicken=1.5, interval=None, format = 'eps', pause=2, **kwargs):

    figure = outfile(subfig=subfig, format=format)

    fontsize = 9

    for ax in plt.gcf().get_axes():

        # bolden the axis labels
        a = ax.xaxis.get_label()
        a.set_fontweight('bold')
        ax.set_xlabel(a.get_text())

        a = ax.yaxis.get_label()
        a.set_fontweight('bold')
        ax.set_ylabel(a.get_text())

        if thicken is not None:
            for line in ax.get_lines():
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
            ax.xaxis.set_major_locator(MultipleLocator(interval[0]))
            try:
                ax.yaxis.set_major_locator(MultipleLocator(interval[0]))
            except:
                pass
            try:
                ax.zaxis.set_major_locator(MultipleLocator(interval[0]))
            except:
                pass

        try:
            a = ax.zaxis.get_label()
            a.set_fontweight('bold')
            ax.set_zlabel(a.get_text())
        except BaseException:
            pass

    # save it
    print('saving --> ', figure)

    plt.savefig(figure, format=format)

    if pause > 0:
        plt.pause(pause)

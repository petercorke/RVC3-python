#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

class Cursor:
    """
    A cross hair cursor.
    """
    def __init__(self, ax, ax2):
        self.ax = ax
        self.ax2 = ax2
        self.horizontal_line = ax.axhline(color='k', lw=0.8)
        self.horizontal_line2 = ax2.axhline(color='k', lw=0.8)
        self.vertical_line = ax.axvline(color='k', lw=0.8)
        self.vertical_line2 = ax2.axvline(color='k', lw=0.8)
        self.vertical_line3 = ax2.axvline(color='k', lw=0.8, ls='--')
        self.leftclicked = False
        self.x_left = None

        # text location in axes coordinates
        self.text = self.ax2.text(0.05, 0.95, '', transform=ax2.transAxes,
            backgroundcolor='w')

    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.horizontal_line2.set_visible(visible)

        self.vertical_line.set_visible(visible)
        self.vertical_line2.set_visible(visible)
        self.vertical_line3.set_visible(visible)

        self.text.set_visible(visible)
        return need_redraw

    def on_mouse_move(self, event):
        if event.inaxes == self.ax2 and self.leftclicked:
            x, y = event.xdata, event.ydata
            # update the line positions
            self.vertical_line3.set_xdata(x)
            self.text.set_text('d={:.2f}'.format(self.x_left - x))
            self.ax2.figure.canvas.draw()
        # if  event.inaxes:
        #     need_redraw = self.set_cross_hair_visible(False)
        #     if need_redraw:
        #         self.ax.figure.canvas.draw()
        # else:
        #     self.set_cross_hair_visible(True)
        #     x, y = event.xdata, event.ydata
        #     # update the line positions
        #     self.horizontal_line.set_ydata(y)
        #     self.vertical_line.set_xdata(x)
        #     # self.text.set_text('x=%1.2f, y=%1.2f' % (x, y))
        #     self.ax.figure.canvas.draw()

    def on_click(self, event):
        # if not event.inaxes:
        #     need_redraw = self.set_cross_hair_visible(False)
        #     if need_redraw:
        #         self.ax.figure.canvas.draw()
        # else:
        if event.inaxes == self.ax:
            self.set_cross_hair_visible(True)
            x, y = event.xdata, event.ydata
            # update the line positions
            self.horizontal_line.set_ydata(y)
            self.vertical_line.set_xdata(x)
            self.horizontal_line2.set_ydata(y)
            self.vertical_line2.set_xdata(x)
            self.ax.figure.canvas.draw()
            self.leftclicked = True
            self.x_left = x

L = Image.Read('rocks2-l.png', reduce=2)
R = Image.Read('rocks2-r.png', reduce=2)


fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=True)

L.disp(ax=ax1, grid=True)
R.disp(ax=ax2, grid=True)
# widgets.Cursor(ax1, horizOn=True, vertOn=True, useblit=False, color='red', linewidth=2)
# stdisp(L, R)

cursor = Cursor(ax1, ax2)
fig.canvas.mpl_connect('motion_notify_event', cursor.on_mouse_move)
fig.canvas.mpl_connect('button_press_event', cursor.on_click)
#print -dsvg ../figs/fig14_20.svg
# plt.show(block=True)
plt.pause(30)
rvcprint.rvcprint()

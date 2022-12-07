# http://paulbourke.net/dataformats/hershey/
import math
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np
import json

"""
Read Hershey JH-format font data and create a cell array that maps ASCII code
to stroke data.

Each character is drawn within a 1x1 grid, with origin at the bottom left.

hershey{'B'} is a struct with elements:
    - width, width of the character
    - height, height of the character
    - top, largest y-coordinate
    - bottom, smallest y-coordinate
    - stroke, 2xN array of waypoints.  A column of NaNs indicates the end of
      one stroke and the beginning of the next.

Hershey's original fonts were encoded in a compact ASCII format by
James Hurt (JH).

References:
    - `Wikipedia <https://en.wikipedia.org/wiki/Hershey_fonts>`_
    - `Hershey vector fonts library, tools, and glyphs <https://github.com/kamalmostafa/hershey-fonts>`_
    - `Hershey Vector Font by Paul Bourke <http://paulbourke.net/dataformats/hershey>`_
"""

## READ the glyph indices
#
# this file lists the glyph indices in ASCII order, starting at 32 (space)
# comprises numbers N and ranges N-M
with open('roman-simplex.txt', 'r') as f:

    fontmap = []

    for number in f.read().split():
        if '-' in number:
            s = list(map(int, number.split('-')))
            fontmap.extend(range(s[0], s[1]+1))
        else:
            fontmap.append(int(number))

# we now have a list of glyph indices in ASCII code order, starting at 32

## READ the glyph data
#
# read lines, each line has a maximum width of 72 chars
# lines of 72 chars have implicit continuation lines
# line[:5] is the glyph number

glyphdata = {}

with open('hershey.txt', 'r') as f:
    longline = None
    for line in f:
        line = line.rstrip()
        if len(line) == 0:
            continue
        if longline is None:
            longline = line
        else:
            longline += line
        if len(line) == 72:
            continue
        fn = int(longline[:5])
        glyphdata[fn] = longline
        longline = None

# glyphdict[glyphindex] -> glyph data

hdict = {}
hershey = namedtuple('hershey', 'strokes width top bottom')

for i, glyphindex in enumerate(fontmap):

    data = glyphdata[glyphindex]
    npairs = int(data[5:8]) - 1
    left = ord(data[8]) - ord('R')
    right = ord(data[9]) - ord('R')
    stroke = []
    data = data[10:]

    strokes = []
    ydata = []

    # build a list of continuous strokes, each is a list of (x,y) data
    for _ in range(npairs):
        pair = data[:2]
        data = data[2:]

        if pair == ' R':
            # end of a stroke
            strokes.append(stroke)
            stroke = []
        else:
            # part of a stroke
            x = ord(pair[0]) - ord('R') - left
            y = ord(pair[1]) - ord('R') + 9            
            stroke.append((x / 25, -y / 25))
            ydata.append(y)

    if len(stroke) > 0:
        strokes.append(stroke)
    width = right - left
    if len(ydata) > 0:
        top = max(ydata)
        bottom = min(ydata)
    else:
        top = 0
        bottom = 0

    width = (right - left) / 25

    hdict[chr(i+32)] = {
        'strokes': strokes,
        'width': width,
        'top': top / 25,
        'bottom': bottom / 25
    }

    # plt.figure()
    # if len(strokes) > 0:
    #     for stroke in strokes:
    #         xy = np.r_[stroke]
    #         plt.plot(xy[:,0], xy[:,1], linewidth=4)
    #     plt.xlim(0,1.5)
    #     plt.ylim(-1,0.5)
    #     plt.title(chr(i+32))

    # plt.pause(0.2)
        
#pickle.dump(hdict, open("hershey.pickle", 'wb'))
json.dump(hdict, open("hershey.json", 'w'))

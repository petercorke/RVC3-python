#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import pytesseract

castle = Image.Read('penguins.png')
# roi = [420, 1000, 0, 900]
castle.disp()

s = pytesseract.image_to_string(castle.image)
print(s)
ocr = pytesseract.image_to_data(castle.image,output_type=pytesseract.Output.DICT)
print(ocr)
for i, conf in enumerate(ocr['conf']):
    if conf == '-1':
        continue
    if conf < 50:
        continue

    plot_labelbox(
        ocr['text'][i],
        tl=(ocr['left'][i], ocr['top'][i]),
        wh=(ocr['width'][i], ocr['height'][i]),
        color='y',
        linestyle='--')
    print(conf, ocr['text'][i])


rvcprint.rvcprint()

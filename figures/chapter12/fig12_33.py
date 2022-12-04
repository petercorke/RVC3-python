#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import pytesseract

penguins = Image.Read('penguins.png')
# penguins.ithresh()%
plt.show(block=True)
# roi = [420, 1000, 0, 900]
penguins.disp()
rvcprint.rvcprint(subfig='a')


# s = pytesseract.image_to_string(penguins.image)
# print(s)
ocr = pytesseract.image_to_data(penguins.image < 100, output_type=pytesseract.Output.DICT)
for text, conf in zip(ocr['text'], ocr['conf']):
    if conf == '-1':
        continue
    if text.strip() == '':
        continue
    print(conf, text)

penguins.disp()
for i, (text, confidence) in enumerate(zip(ocr['text'], ocr['conf'])):
    # if conf == '-1':
    #     continue

    # top is the minimum v-coordinate
    if text.strip() != '' and confidence > 50:
        plot_labelbox(
            ocr['text'][i],
            lb=(ocr['left'][i], ocr['top'][i]),
            wh=(ocr['width'][i], ocr['height'][i]),
            color='y',
            filled=True,
            alpha=0.2,
            linestyle='--')


rvcprint.rvcprint(subfig='b')


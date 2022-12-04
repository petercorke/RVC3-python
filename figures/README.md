# Figure generation scripts

The code examples in the book contain the essential commands to generate most
of the figures.  What they leave out are the fiddly Matplotlib commands to set
colors, line styles, axis labels, legends etc.  All that detail is given in
these Python scripts which generated the actual figures included in the book.

Each chapter is located in a folder `chapterN` which contains:

- `figN_M.py`  the script to generate Fig. N.M
- `box_NAME.py`  the script to generate a figure in an excurse box

The files are executable and can be run by
```
$ ./figN_M.py
```
or
```
$ python figN_M.py
```

By default the figures
are saved in the current folder with a root name `figN_M` in PDF format.
For example
```
% python code/RVC3-python/figures/chapter10/fig10_20.py
saving -->  fig10_20.pdf
```

Some files generate multiple sub-figures with lowercase letter suffixes.

All these files use `RVC3.tools.rvcprint` to save the created files.  The
package `rvcpython` must have been installed. 

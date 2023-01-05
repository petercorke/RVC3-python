# Figure generation scripts

Most of the figures in the book have been generated using Matplotlib.  The code
examples in the book contain the essential commands to generate most of the
figures, but they leave out the fiddly Matplotlib commands to set colors, line
styles, axis labels, legends etc.  That would make the code examples too long,
and get in the way of understanding.  So the in-book examples are pretty bare
bones, and all the fiddly detail to make good looking plots is in these Python
scripts which generated the actual figures included in the book.

## Running the scripts

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




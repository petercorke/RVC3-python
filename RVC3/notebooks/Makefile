# convert Python scripts to Jupyter notebooks
%.ipynb : %.py
	jupytext --to ipynb $<

all: $(subst py,ipynb,$(wildcard *.py))

.FORCE:

BLUE=\033[0;34m
BLACK=\033[0;30m

help:
	@echo "$(BLUE) make dist - build dist files"
	@echo " make upload - upload to PyPI"
	@echo " make clean - remove dist and docs build files"
	@echo " make help - this message$(BLACK)"

dist: .FORCE
	# $(MAKE) test
	python -m build
	ls -lh dist/rvc3python-*

upload: .FORCE
	twine upload dist/*

clean: .FORCE
	-rm -r *.egg-info
	-rm -r dist


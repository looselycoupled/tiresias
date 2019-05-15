# Shell to use with Make
SHELL := /bin/bash

# Set important Paths
PROJECT := tiresias

# Export targets not associated with files
.PHONY: clean archive

# Clean build files
clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	find . -name "__pycache__" -print0 | xargs -0 rm -rf
	-rm -rf htmlcov
	-rm -rf .coverage*
	-rm -rf build
	-rm -rf dist
	-rm -rf $(PROJECT).egg-info
	-rm -rf .eggs

archive:
	zip -r data-`date +%F-%H%M%S.zip` data/*
	-rm -rf data/

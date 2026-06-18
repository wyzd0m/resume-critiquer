# Makefile — shortcuts for common tasks
# Usage: make install   → install dependencies
#        make run       → start the app
#        make help      → list all commands

.PHONY: help install run

help:
	@echo ""
	@echo "Available commands:"
	@echo "  make install   Install all Python dependencies"
	@echo "  make run       Start the Streamlit app locally"
	@echo ""

install:
	pip install -r requirements.txt

run:
	streamlit run app.py

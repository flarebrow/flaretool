export PYTHONPATH=./repos/
sphinx-apidoc -f -o ./docs_src ./repos/flaretool
sphinx-build ./docs_src ./docs

# sphinx-apidoc -f -o ./docs_src ./repos/flaretool
export PYTHONPATH=./repos/
sphinx-build ./docs_src ./docs

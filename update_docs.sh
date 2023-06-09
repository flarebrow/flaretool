export PYTHONPATH=./repos/
rm ./docs_src/f*.rst
sphinx-apidoc -f -o ./docs_src ./repos/flaretool
sphinx-build ./docs_src ./docs

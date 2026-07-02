export PYTHONPATH=./src/
rm ./docs_src/f*.rst
sphinx-apidoc -f -o ./docs_src ./src/flaretool
sphinx-build ./docs_src ./docs
touch ./docs/.nojekyll
touch ./docs/.docs

#!/bin/bash

mkdir -p _site
for notebook in $(find . -name "*.ipynb" ! -path "./.ipynb_checkpoints/*"); do
jupyter nbconvert --to html "$notebook" --output-dir _site/
done
# Create an index page
echo "<html><body><h1>Jupyter Notebooks</h1><ul>" > _site/index.html
for file in _site/*.html; do
if [ "$(basename "$file")" != "index.html" ]; then
    echo "<li><a href=\"$(basename "$file")\">${file%.*}</a></li>" >> _site/index.html
fi
done
echo "</ul></body></html>" >> _site/index.html
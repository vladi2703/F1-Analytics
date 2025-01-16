#!/bin/bash

mkdir -p _site

mkdir -p _site/assets/images
cp assets/images/* _site/assets/images/

cp assets/templates/index.html _site/

for notebook in $(find . -name "*.ipynb" ! -path "./.ipynb_checkpoints/*"); do
    jupyter nbconvert --to html --execute "$notebook" --output-dir _site/
done

echo "Site generation complete. Check _site directory for the results."
#!/bin/sh

cd ..
python setup.py sdist
mv dist tools/
mv testvibe.egg-info tools/
#!/bin/sh

cd ..
python setup.py sdist
mv dist testvibe.egg-info tools/
cd tools
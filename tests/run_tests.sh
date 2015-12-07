#!/bin/sh

export PYTHONPATH=../

nosetests --with-coverage --cover-package=testvibe --cover-inclusive \
          --cover-erase

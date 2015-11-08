Testvibe
========

Testvibe is a high-level Python test framework designed for RESTful JSON APIs.

Robust and seamless, making developers, managers happy

It can test production as well as pre-deploy and for longevity.

Acceptance
Performance
Longevity
Scale

Great logging

Supports:
  * Authentication
  * Reporting

Getting started
===============

Installation
------------
The easiest way to install testvibe is with pip::

    pip install testvibe

but it can also be downloaded straight from Github at
https://github.com/Niklas9/testvibe.

Your first testvibe project
---------------------------
The first time you're using testvibe, you'll have to take care of some initial
setup. Namely, you'll need to auto-generate some code that establishes a
testvibe project - a collection of settings for an instance of testvibe,
including testvibe specific options as well as application settings.

From the command line, run the following command

    $ tvctl startproject mytests

this will create a mytests directory in your current directory.

The first step after this is usually to add a test group, run the following
command inside the mytests directory

    $ tvctl addtestgroup my_testgroup

Project file/directory structure
--------------------------------
~/mytests
|--settings.py
|--my_testgroup
   |---RUNLIST
   |---test_suite.py

Test structure
--------------
Tests are structured into three groups:

    * Test groups
        * Test suites
            * Test cases

For example, to test a full application test groups could be
acceptance/performance/scale, but it can also be the names of different micro
services.

See full documentation for more options on constructing test suites with common
setup and teardown for each test case, , etc.

Creating your first test case
-----------------------------
Before creating the actual 

Running your tests
------------------
Executing your tests by simply from your project directory

    $ tvctl run

This will look for all directories having a RUNLIST named file in them, and
executed them synchronously in given order.

See full documentation for more options on parallelization, reporting, longevity, scale etc.

License
=======

Contributing
============

This project accepts contributions via GitHub pull requests. Please check issues
first to make sure noone else is working on the same thing.

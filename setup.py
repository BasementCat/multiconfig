#!/usr/bin/env python
import os
from setuptools import setup

def read(filen):
    with open(os.path.join(os.path.dirname(__file__), filen), "r") as fp:
        return fp.read()
 
setup (
    name = "multiconfig",
    version = "0.2",
    description="Hierarchical configuration library for Python, supporting cascading configuration files",
    long_description=read("README.md"),
    author="Alec Elton",
    author_email="alec.elton@gmail.com", # Removed to limit spam harvesting.
    url="http://github.com/basementcat/multiconfig",
    packages=["multiconfig", "tests"],
    test_suite="nose.collector",
    install_requires=["PyYAML"],
    tests_require=["nose"]
)
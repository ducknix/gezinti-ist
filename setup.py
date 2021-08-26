#!/usr/bin/env python
# coding: utf-8
from setuptools import setup
from Cython.Build import cythonize

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name="Gezinti.ist",
    version="1.0",
    description="Çevrenizi keşfedin",
    long_description=long_description,
    author="Özgür Savaş (@ducknix)",
    author_email="touch00xf@gmail.com",
    license="Unlicense",
    packages=[
        "Flask",
        "geopy",
        "mysql-connector-python"
    ],
    ext_modules=cythonize(["src/views/*.pyx", "src/scripts/*.pyx"],
                          build_dir="build")
)

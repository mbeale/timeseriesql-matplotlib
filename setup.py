#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="timeseriesql-matplotlib",
    version="0.0.2",
    description="A plotting backend for the TimeSeriesQL library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/mbeale/timeseriesql-matplotlib",
    author="Michael Beale",
    author_email="michael.beale@gmail.com",
    license="MIT",
    packages=["timeseriesql_matplotlib"],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    install_requires=["timeseriesql", "matplotlib"],
    python_requires=">=3.6",
)


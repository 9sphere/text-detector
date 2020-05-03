#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="text-detector",
    version="0.0.2",
    author="Muthu krishnan",
    author_email="muthukrishnan749@gmail.com",
    description="Locating texts in images using computer vision",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muthuspark/text-detector",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
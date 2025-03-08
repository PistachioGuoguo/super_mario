#!/usr/bin/env python3

import setuptools

PACKAGE_NAME = "super_mario"
DESCRIPTION = "A super mario pygame"


setuptools.setup(
    name=PACKAGE_NAME,
    version="0.0.0",
    package_data={PACKAGE_NAME: ["py.typed", "config/*.json", "templates/*.pdf"]},
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    description=DESCRIPTION,
    entry_points={
        "console_scripts": [
            "mario = super_mario.mario:main",
        ]
    },
)

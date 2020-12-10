#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='beets-funkwhaleupdate',
    version='0.0.1',
    description='Update Funkwhale when album is imported by beets.',
    author='Andreas Kind',
    author_email='andreas.kind@ghosttown-productions.de',
    license='MIT',

    package_dir={"": "src"},

    packages=[
        'beetsplug/funkwhaleupdate',
    ],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)

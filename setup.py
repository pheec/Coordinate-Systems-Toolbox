#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='coordinate_structure_toolbox',
    version='0.1.0',
    author='Tomáš Fiala',
    author_email='your.email@example.com', #TODO change
    description='An example Python package', #TODO change
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pheec/Coordinate-Systems-Toolbox',
    packages=find_packages(exclude=('tests*', 'docs')),
    install_requires=[
        'numpy>=1.18.5',
        'requests>=2.24.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
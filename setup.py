__author__ = 'walter'
# -*- coding: utf-8 -*-

#This is just a work-around for a Python2.7 issue causing
#interpreter crash at exit when trying to log an info message.
try:
    import logging
    import multiprocessing
except:
    pass

import sys
py_version = sys.version_info[:2]

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

testpkgs=[]

dependency_links = []

install_requires=[
    "Flask",
    "pymongo",
    "simplejson",
    "Werkzeug",
    "requests",
    "Pillow",
    "yuicompressor",
    "fabric",
    "click"
]

setup(
    name='bombolone',
    version='0.3.4',
    description='Bombolone is a tasty Content Management System for Python based on Flask',
    author='Leonardo Zizzamia',
    author_email='leonardo@zizzamia.com',
    packages=find_packages(),
    dependency_links=dependency_links,
    install_requires=install_requires,
    include_package_data=True,
    package_data={'bombolone': ['static/*/*/*/*/*',
                                'data/*/*/*/*/*/*',
                                'dump/*/*',
                                'templates/*/*/*']},
    tests_require=testpkgs,
    entry_points={
        'console_scripts': [
            'bombolone = bombolone:main'
        ],
    },
    zip_safe=False
)

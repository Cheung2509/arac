#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-


from __future__ import absolute_import
__author__ = 'Justin S Bayer, bayer.justin@googlemail.com'


from aracsetuphelpers import (make_compiler, compile_arac, compile_test, 
    compile_swig)

  
setup(
    name="arac",
    version="0.1post",
    description="Arac is a C++ library for modular neural networking.",
    license="BSD",
    keywords="Neural Networks Machine Learning",
    packages=['./src/python',],
    include_package_data=True,
    package_dir={'arac': './src/python/arac'},
    data_files=[('arac', ('libarac.dylib',))],
    test_suite='arac.tests.runtests.make_test_suite',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    install_requires=[
        'requests', 'six'
    ]
)
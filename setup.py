# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except:
    from distutils.core import setup

from calldules import __doc__


setup(
    name='calldules',
    version='1.0',
    url='https://github.com/Ivoz/calldules/',
    license='MIT',
    author='Matthew Iversen',
    author_email='matt@notevencode.com',
    description='making modules callable, for not very good reasons.',
    long_description=__doc__,
    py_modules=['calldules'],
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Utilities'
    ],
)

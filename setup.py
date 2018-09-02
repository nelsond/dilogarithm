from setuptools import setup, find_packages
import os

import numpy
from numpy.distutils.extension import Extension as NumpyExtension

here = os.path.dirname(os.path.abspath(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

with open(os.path.join(here, 'requirements', 'common.txt')) as f:
    required = f.read().splitlines()

ext_dir = os.path.join(here, 'dilogarithm', 'ext')

setup(
    name='dilogarithm',

    use_scm_version=True,
    setup_requires=['setuptools_scm', 'numpy'],

    description='Fairly fast implementation of the Dilogarithm for numpy',
    long_description=long_description,

    url='https://github.com/nelsond/dilogarithm',

    author='Nelson Darkwah Oppong',
    author_email='n@darkwahoppong.com',

    license='GNU GPL',

    classifiers=[
        'Development Status :: 4 - Beta',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.4'
    ],

    keywords='dilogarithm polylogarithm polylog polylog2 numpy',

    packages=find_packages(),
    include_package_data=True,

    install_requires=required,

    ext_modules=[NumpyExtension(
                    'dilogarithm',
                    sources=[os.path.join(ext_dir, 'rdilogmodule.c')],
                    include_dirs=[numpy.get_include()])],
)

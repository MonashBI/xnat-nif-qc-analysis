import sys
import os.path
from setuptools import setup, find_packages


PACKAGE_NAME = 'xnat_nif_qc_analysis'

# Get version from module inside package
sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                PACKAGE_NAME))
from package_info import __version__  # @UnresolvedImport @IgnorePep8
sys.path.pop(0)

setup(
    name=PACKAGE_NAME,
    version=__version__,
    author='Tom G. Close',
    author_email='tom.g.close@gmail.com',
    packages=find_packages(),
    url='https://github.com/mbi-image/xnat-nif-qc-analysis',
    license='The MIT License (MIT)',
    description=(
        'A package for analysing QC data collected according to the'
        'NIF-TDRS SOP'),
    long_description=open('README.rst').read(),
    install_requires=['nianalysis>=0.1'],
    dependency_links=[
        "git+https://github.com/mbi-image/nianalysis"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps."])

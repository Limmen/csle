#!/usr/bin/env python
# -*- coding: utf-8 -*-

descr = """
"""

import os
import sys
from os.path import join

DISTNAME = "scikits.optimization"
DESCRIPTION = "A python module for numerical optimization"
LONG_DESCRIPTION = descr
MAINTAINER = "Matthieu Brucher"
MAINTAINER_EMAIL = "matthieu.brucher@gmail.com"
URL = "http://projects.scipy.org/scipy/scikits"
LICENSE = "new BSD"

optimization_version = 0.3

import os
import shutil
import string
import sys
from distutils.errors import DistutilsError

import setuptools
from numpy.distutils.core import Extension, setup
from numpy.distutils.system_info import NotFoundError, dict_append, so_ext, system_info

DOC_FILES = []


def configuration(parent_package="", top_path=None, package_name=DISTNAME):
    if os.path.exists("MANIFEST"):
        os.remove("MANIFEST")
    pkg_prefix_dir = os.path.join("scikits", "optimization")

    from numpy.distutils.misc_util import Configuration

    config = Configuration(
        package_name,
        parent_package,
        top_path,
        version=optimization_version,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        long_description=LONG_DESCRIPTION,
    )

    return config


if __name__ == "__main__":
    setup(
        configuration=configuration,
        install_requires="numpy",  # can also add version specifiers
        namespace_packages=["scikits"],
        packages=setuptools.find_packages(),
        include_package_data=True,
        test_suite="",  # "scikits.openopt.tests", # for python setup.py test
        zip_safe=False,  # the package can run out of an .egg file
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Topic :: Scientific/Engineering",
        ],
    )

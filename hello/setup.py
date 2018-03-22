# To build the extension, run this setup script like so:
#
#    python setup.py build_ext --inplace
#
# or on Windows:
#
#    python setup.py build_ext --inplace --compiler=msvc
#
# To produce html annotation for a cython file, instead run:
#     cython -a myfile.pyx

import sys
PY2 = sys.version_info.major == 2

# Setuptools monkeypatches distutils to be able to find the visual C compiler on
# windows:
import setuptools
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import platform

if PY2:
    PY2_SUFFIX = '_py27_{}_{}'.format(sys.platform, platform.architecture()[0])
else:
    PY2_SUFFIX = ''

ext_modules = [Extension("hello" + PY2_SUFFIX, ["hello.pyx"])]
setup(
    name = "hello" + PY2_SUFFIX,
    cmdclass = {"build_ext": build_ext},
    ext_modules = ext_modules,
)

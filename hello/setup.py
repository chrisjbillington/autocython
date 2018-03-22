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

# Setuptools monkeypatches distutils to be able to find the visual C compiler on
# windows:
import setuptools
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("hello", ["hello.pyx"])]
setup(
    name = "hello",
    cmdclass = {"build_ext": build_ext},
    ext_modules = ext_modules,
)

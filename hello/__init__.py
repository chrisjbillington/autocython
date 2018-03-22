from __future__ import print_function, unicode_literals, division, absolute_import
import sys
import platform
import importlib
PY2 = sys.version_info.major == 2
if PY2:
    str = unicode

if PY2:
    PY2_SUFFIX = '_py27_{}_{}'.format(sys.platform, platform.architecture()[0])
else:
    PY2_SUFFIX = ''

def ensure_extensions_compiled(names, msg=None):
    """Ensure the Cython extensions with the given list of names is compiled, and
    compile by running setup.py if not. Print msg to stderr if compilation is
    required. Assumes that python 2 files have a suffix PY2_SUFFIX so that .so and
    .pyd files can exist in the same folder for multiple platforms. This is not
    neccesary on Python 3, which does this already."""
    import os
    import shutil
    from os.path import exists, getmtime
    from distutils.sysconfig import get_config_var
    if isinstance(names, str) or isinstance(names, bytes):
        names = [names]
    this_folder = os.path.dirname(os.path.abspath(__file__))
    for name in names:
        extension_pyx = os.path.join(this_folder, name + '.pyx')
        extension_so = os.path.join(this_folder, name)
        ext_suffix = get_config_var('EXT_SUFFIX')
        if ext_suffix is None:
            if os.name == 'nt':
                ext_suffix = '.pyd'
            else:
                ext_suffix = '.so'
        extension_so = extension_so + PY2_SUFFIX + ext_suffix
        extension_c = os.path.join(this_folder, name + '.c')
        if (not exists(extension_so)
                or getmtime(extension_so) < getmtime(extension_pyx)):
            current_folder = os.getcwd()
            if msg is not None:
                sys.stderr.write(msg + '\n')
            try:
                os.chdir(this_folder)
                cmd = sys.executable + " setup.py build_ext --inplace"
                if os.name == 'nt':
                    cmd += ' --compiler=msvc'
                if os.system(cmd) != 0:
                    msg = ' '.join(s.strip() for s in """Couldn't compile cython
                          extension. If you are on Windows, ensure you have the
                          following conda packages: libpython, cython, and have
                          installed the appropriate Microsoft Visual C or Visual
                          Studio Build Tools for your version of Python. If on
                          another platform, ensure you have gcc, libpython, and
                          cython, from conda or otherwise. See above for the
                          specific error that occured""")
                    raise RuntimeError(msg)
                try:
                    shutil.rmtree('build')
                except Exception:
                    pass
                try:
                    os.unlink(extension_c)
                except Exception:
                    pass
            finally:
                os.chdir(current_folder)


def import_extension(name):
    """Import the extension, abstracting the platform"""
    name = name + PY2_SUFFIX
    return importlib.import_module(__name__ + '.' + name)


ensure_extensions_compiled(['hello'], 'Extension not compiled, compiling...')
module = import_extension('hello')
hello = module.hello
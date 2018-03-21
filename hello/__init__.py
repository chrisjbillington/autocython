from __future__ import print_function, unicode_literals, division, absolute_import
import sys
if sys.version_info.major == 2:
    str = unicode

def ensure_extensions_compiled(names):
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
        extension_so += ext_suffix
        extension_c = os.path.join(this_folder, name + '.c')
        if (not exists(extension_so)
                or getmtime(extension_so) < getmtime(extension_pyx)):
            current_folder = os.getcwd()
            try:
                os.chdir(this_folder)
                cmd = sys.executable + " setup.py build_ext --inplace"
                if os.name == 'nt':
                    cmd += ' --compiler=mingw32'
                if os.system(cmd) != 0:
                    msg = ("Couldn't compile cython extension. If you are on " +
                           "Windows, ensure you have the following conda " +
                           "packages: mingw, libpython, cython")
                    raise RuntimeError(msg)
                shutil.rmtree('build')
                os.unlink(extension_c)
            finally:
                os.chdir(current_folder)

ensure_extensions_compiled(['hello'])

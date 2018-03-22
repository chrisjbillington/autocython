from __future__ import print_function, unicode_literals, division, absolute_import
import sys
import os
import platform
import importlib
import json
import shutil
import hashlib
PY2 = sys.version_info.major == 2
if PY2:
    str = unicode


if PY2:
    PY2_SUFFIX = b'_py27_{}_{}'.format(sys.platform, platform.architecture()[0])
else:
    PY2_SUFFIX = ''


def file_hash(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
      for b in iter(lambda : f.read(128*1024), b''):
        h.update(b)
    return h.hexdigest()


def compute_hashes(pyx_files, so_files):
    hashes = {}
    for pyx_file, so_file in zip(pyx_files, so_files):
        if os.path.exists(so_file):
            so_relpath = os.path.split(so_file)[1]
            hashes[so_relpath] = {'pyx': file_hash(pyx_file),
                                  'so': file_hash(so_file)}
    return hashes


def get_last_compile_state(folder):
    try:
        with open(os.path.join(folder, 'compile_state.json'), 'r') as f:
            return json.load(f)
    except (IOError, ValueError):
        return {}


def save_compile_state(folder, compile_state):
    with open(os.path.join(folder, 'compile_state.json'), 'w') as f:
        json.dump(compile_state, f, indent=4, sort_keys=True)


def hashes_valid(folder, pyx_files, so_files):
    """Check if the compiled extensions are valid, by comparing the hash of the pyx
    files and so files at last compilation to what they are now. Return False if
    any so file does not exist or has a different hash"""
    compile_state = get_last_compile_state(folder)
    current_state = compute_hashes(pyx_files, so_files)
    for so_file in so_files:
        so_relpath = os.path.split(so_file)[1]
        if so_relpath not in compile_state or so_relpath not in current_state:
            return False
        if current_state[so_relpath] != compile_state[so_relpath]:
            return False
    return True


def update_hashes(folder, pyx_files, so_files):
    compile_state = get_last_compile_state(folder)
    current_state = compute_hashes(pyx_files, so_files)
    for so_relpath in list(compile_state.keys()):
        if not os.path.exists(os.path.join(folder, so_relpath)):
            del compile_state[so_relpath]
    compile_state.update(current_state)
    save_compile_state(folder, compile_state)


def compile_extensions(folder, names):
    """Run setup.py to compile the extensions inplace, then remove the build
    directory and the generated C files"""
    current_folder = os.getcwd()
    try:
        os.chdir(folder)
        cmd = sys.executable + " setup.py build_ext --inplace"
        if os.name == 'nt':
            cmd += ' --compiler=msvc'
        if os.system(cmd) != 0:
            msg = """Couldn't compile cython
                  extension. If you are on Windows, ensure you have the
                  following conda packages: libpython, cython, and have
                  installed the appropriate Microsoft Visual C or Visual
                  Studio Build Tools for your version of Python. If on
                  another platform, ensure you have gcc, libpython, and
                  cython, from conda or otherwise. See above for the
                  specific error that occured"""
            msg = ' '.join(s.strip() for s in msg.splitlines())
            raise RuntimeError(msg)
        try:
            shutil.rmtree('build')
        except Exception:
            pass
        for name in names:
            extension_c = os.path.join(folder, name + '.c')
            try:
                os.unlink(extension_c)
            except Exception:
                pass
    finally:
        os.chdir(current_folder)


def ensure_extensions_compiled(folder, names=None):
    """Ensure the Cython extensions in the given folder with the given list of
    names are compiled, and if not (or if they are in need up recompilation),
    compile them by running setup.py (assumed to be in the same folder). If no
    names are given, they will be inferred from any .pyx files in the folder. It is
    assumed that each cython file is called <name>.pyx, and that each extension (as
    specified in setup.py) is called <name><PY2_SUFFUX>, where PY2_SUFFIX is
    defined at the top of this file, and specifies the platform details for Python
    2, allowing platform_specific_import to import the correct version of the
    extension if multiple versions exist for different platforms. In Python 3
    PY2_SUFFIX is the empty string since Python 3 does this automatically."""
    from distutils.sysconfig import get_config_var
    if isinstance(names, str) or isinstance(names, bytes):
        names = [names]
    if names is None:
        names = [os.path.splitext(name)[0]
                 for name in os.listdir(folder)
                 if name.endswith('.pyx')]
    pyx_files = []
    so_files = []
    for name in names:
        extension_pyx = os.path.join(folder, name + '.pyx')
        extension_so = os.path.join(folder, name)
        ext_suffix = get_config_var('EXT_SUFFIX')
        if ext_suffix is None:
            ext_suffix = '.pyd' if os.name == 'nt' else '.so'
        extension_so = extension_so + PY2_SUFFIX + ext_suffix
        pyx_files.append(extension_pyx)
        so_files.append(extension_so)
    if not hashes_valid(folder, pyx_files, so_files):
        msg = "Extension(s) out of date, recompiling...\n"
        sys.stderr.write(msg)
        compile_extensions(folder, names)
        update_hashes(folder, pyx_files, so_files)


def platform_specific_import(fullname):
    """Import the extension, abstracting the platform. This is not neccesary on
    Python 3."""
    name = fullname + PY2_SUFFIX
    return importlib.import_module(name)
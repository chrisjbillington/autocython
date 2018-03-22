from __future__ import print_function, unicode_literals, division, absolute_import
import sys
PY2 = sys.version_info.major == 2
if PY2:
    str = unicode

from .autocython import (PY2_SUFFIX, ensure_extensions_compiled,
                         platform_specific_import)

__all__ = ['PY2_SUFFIX', 'ensure_extensions_compiled', 'platform_specific_import']
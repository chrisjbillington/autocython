from .autocython import ensure_extensions_compiled, platform_specific_import
import os

this_folder = os.path.dirname(os.path.abspath(__file__))

ensure_extensions_compiled(this_folder)
module = platform_specific_import('hello.hello')
hello = module.hello
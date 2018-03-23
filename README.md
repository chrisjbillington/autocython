My example repo for how to compile Cython extensions for multiple platforms whilst
being able to bundle all precompiled binaries together.

# autocython

Like `pyx_import`, but when you want to write your own setup.py still, and you want to keep the compiled extensions in the package directory.

Supports Python 2.7 and Python 3.5+

"How is that at all like `pyx_import`?" I hear you ask. "Why would I want that?".

Well, `autocython` records a hash of the `.pyx` files and the resulting `.so` or
`.pyd` files whenever it compiles anything, and recompiles automatically (by
running your `setup.py`) if it detects that there is a mismatch. So that's how it's
like `pyx_import`.

The similarities end there. As mentioned, you have to write your own `setup.py`. I
don't see this as much of a drawback, it's rare that I have a Cython extension that
doesn't need at least some customisation in its `setup.py`, and that customisation
might as well go in a separate file than in a call to `pyx_import`. See the example
below for how to write a setup.py that works with `autocython`.

`autocython` expects you to keep all the compiled extensions in the same directory,
even for different versions of Python and platforms. Whilst keeping multiple
versions of extensions for different platforms in the same directory is easy in
Python 3 (since extensions get a platform-specific suffix), it is less easy in
Python 2. So `autocython` provides a platform-specific suffix that you can add to
the names of your extensions in your setup.py (see example below), and an import
function that uses the same suffix to import the right version at run time. This
allows distributing fat packages with all the supported compiled versions of the
extension in the same folder. Whilst it is bad practice to distribute packages like
this, it is often what is most convenient if you're a research group doing
numerical simulations or lab control systems and sharing code with each other
without wanting to think too hard about packaging or build servers.

`autocython` also serves as a reminder to myself as to the current state of
compiling cython extensions on all platform. It calls your `setup.py` as: `python
setup.py build_ext --inplace`, or on Windows as `python setup.py build_ext
--inplace --compiler=msvc`. So long as your `setup.py` imports `setuptools`, on
Windows this means you actually get a meaningful error about where to download the
correct compiler from Microsoft. Even if you get these steps wrong, `autocython`
prints a big fat error message describing what you need to make sure you've done,
which I intend to update whenever the state of Windows compiling changes.

( 
[view on pypi](https://pypi.python.org/pypi/zprocess/);
[view on Bitbucket](https://bitbucket.org/cbillington/zprocess)
)

   * Install `python setup.py install`.


# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2013 Matthew Iversen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
No more from <module> import <Module>!

Wouldn't be nice if...

    >>> import pprint
    >>> pprint("hello")
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    TypeError: 'module' object is not callable

Was possible? Well:

1. Add special sauce::

   >>> import calldules

2. Import module(s), call::

   >>> import pprint
   >>> pprint("hello")

3. ???\?

   ::

      'hello'

4. PROFIT!!!

Also works with such modules as ``flask``, ``codecs``, ``array``, ``datetime``,
``decimal``, ``random``, and many more!

No responsibility is taken for any grievous harm caused either
by irresponsible *or* responsible use of ``calldules``.

Inspired by Richard Jones' talk `Don't Do This`_.

.. _Don't Do This: http://www.youtube.com/watch?v=H2yfXnUb1S4
"""


import ctypes


# Create a function prototype for a 3-arg function
ternaryfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object,
                               ctypes.py_object, ctypes.c_void_p)


# Define a new python type that's callable, via a ternaryfunc
class PyTypeObject(ctypes.Structure):
    _fields_ = (
        ("ob_refcnt", ctypes.c_ssize_t),
        ("ob_type", ctypes.c_void_p),
        ("ob_size", ctypes.c_ssize_t),
        ("tp_name", ctypes.c_char_p),
        ("tp_basicsize", ctypes.c_ssize_t),
        ("tp_itemsize", ctypes.c_ssize_t),
        ("tp_dealloc", ctypes.c_void_p),
        ("tp_print", ctypes.c_void_p),
        ("tp_getattr", ctypes.c_void_p),
        ("tp_setattr", ctypes.c_void_p),
        ("tp_reserved", ctypes.c_void_p),
        ("tp_repr", ctypes.c_void_p),
        ("tp_as_number", ctypes.c_void_p),
        ("tp_as_sequence", ctypes.c_void_p),
        ("tp_as_wrapping", ctypes.c_void_p),
        ("tp_hash", ctypes.c_void_p),
        ("tp_call", ternaryfunc),
        ("tp_str", ctypes.c_void_p),
    )


# And define a python object whose type is the one above
class PyObject(ctypes.Structure):
    _fields_ = (
        ("ob_refcnt", ctypes.c_ssize_t),
        ("ob_type", ctypes.POINTER(PyTypeObject)),
    )


@ternaryfunc
def _module_call(obj, args, kwargs):
    # kwargs are 'special' in ctypes.
    if kwargs:
        kwargs = ctypes.cast(kwargs, ctypes.py_object).value
    else:
        kwargs = {}
    name = obj.__name__
    guesses = [name.title(), name]
    if name.endswith('s'):
        name = name.rstrip('s')
        guesses += [name.title(), name]
    guesses = [p for p in guesses if hasattr(obj, p)]
    if len(guesses) == 0:
        return
    prop = getattr(obj, guesses[0])
    # HERE GOES!
    return prop(*args, **kwargs)

# Load a module object into our new PyObject
ctypes_mod = PyObject.from_address(id(ctypes))
# Grab its type's contents
ctypes_mod_ob_type = ctypes_mod.ob_type.contents
# Assign its callable slot to _module_call()
ctypes_mod_ob_type.tp_call = _module_call

# HERE BE MODRAGONS, BEWARE ALL YE WHO IMPORT.

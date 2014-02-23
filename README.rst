Calldules!
==========

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

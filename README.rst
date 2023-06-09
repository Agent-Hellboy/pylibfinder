pylibfinder (currently supports 3.10 and 3.11 on posix)
===========

- pylibfinder is a Python library that allows you to spot a keyword as a function inside the Python standard library. 
- It provides a convenient way to search for functions that match a given keyword within the standard library modules.
- With pylibfinder, you can easily identify the modules and functions that are available in Python and gain insights  into their usage and availability. 
- This library is designed to assist developers in finding relevant functions and understanding the   Python standard library better.


.. image:: https://img.shields.io/pypi/v/pylibfinder
   :target: https://pypi.python.org/pypi/pylibfinder/

.. image:: https://github.com/Agent-Hellboy/pylibfinder/actions/workflows/python-package.yml/badge.svg
    :target: https://github.com/Agent-Hellboy/pylibfinder/
    
.. image:: https://img.shields.io/pypi/pyversions/pylibfinder.svg
   :target: https://pypi.python.org/pypi/pylibfinder/

.. image:: https://img.shields.io/pypi/l/pylibfinder.svg
   :target: https://pypi.python.org/pypi/pylibfinder/

.. image:: https://pepy.tech/badge/pylibfinder
   :target: https://pepy.tech/project/pylibfinder

.. image:: https://img.shields.io/pypi/format/pylibfinder.svg
   :target: https://pypi.python.org/pypi/pylibfinder/

Installation
============
 

For stable version

        - clone the repo cd `pylibfinder` then do python3 setup.py install (on Mac and linux)

For developement

        - git clone https://github.com/Agent-Hellboy/pylibfinder
        - cd pylibfinder
        - make changes in funcfinder.c 
        - compile it using `gcc -shared -o funcfinder.so -fPIC -I /usr/include/python3.12 funcfinder.c`
        - it will generate a funcfinder.so 
        - open repl and test  


Example
=======

.. code:: py

      >>> import funcfinder
      >>> funcfinder.get_module('literal')
      [{'Module': 'ast', 'Function': 'literal_eval'}, {'Module': 're._compiler', 'Function': '_get_literal_prefix'}]
      >>> 



Contributing
============

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

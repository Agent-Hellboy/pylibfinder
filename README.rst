spotter
=======

Library to spot a keyword as a function inside python stdlib


Installation
============
 
   - git clone https://github.com/Agent-Hellboy/spotter
   - cd spotter
   - sudo python3 setup.py install 

Example
=======

.. code:: py

      The library provides an API to find where function like print is defined 
      >>> spotter.get_module('print')
      Keyword: print
      Module: builtins, Function: print


      >>> spotter.get_module('literal')
      Keyword: literal
      Module: ast, Function: literal_eval
      Module: re._compiler, Function: _get_literal_prefix


Contributing
============

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

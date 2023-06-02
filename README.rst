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

      >>> import spotter
      >>> spotter.get_module('literal')
      [{'Module': 'ast', 'Function': 'literal_eval'}, {'Module': 're._compiler', 'Function': '_get_literal_prefix'}]
      >>> 


Development 
============
make changes in spotter.c 
compile it using `gcc -shared -o spotter.so -fPIC -I /usr/include/python3.12 spotter.c`
it will generate a spotter.so 
open repl and test  

Contributing
============

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

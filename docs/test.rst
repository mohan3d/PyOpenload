============
Testing
============

Requirements
============

``OPENLOAD_LOGIN`` and ``OPENLOAD_KEY`` must be in your environment variables.

You may export them in **linux**

.. code-block:: bash

    export OPENLOAD_LOGIN=<YOUR API LOGIN>
    export OPENLOAD_KEY=<YOUR API KEY>


It is prefered to create new folder in `openload file manager <https://openload.co/account#fileman>`_
before starting tests.

.. note:: You can find OPENLOAD_LOGIN (API Login) and OPENLOAD_KEY (API Key) in openload User Panel at the
    `User Settings <https://openload.co/account#usersettings>`_.


Testing
=======

In the root directory of PyOpenload.

.. code-block:: bash

    $ python -m unittest tests/test_openload.py


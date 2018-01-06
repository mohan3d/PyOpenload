PyOpenload |StarButton|
=======================

python wrapper for `Openload.co`_ `API`_.

|travis| |pypi| |format| |CodacyBadge| |license|

Install
-------

.. code-block:: bash

    $ pip install pyopenload


Usage
-----

All `API`_ features are implemented.

**Retrieve account info**

.. code:: python

    from openload import OpenLoad

    ol = OpenLoad('login', 'key')

    account_info = ol.account_info()
    print(account_info)


**Upload file**

.. code:: python

    from openload import OpenLoad

    ol = OpenLoad('login', 'key')

    uploaded_file_info = ol.upload_file('/home/username/file.txt')
    print(uploaded_file_info)


**Retrieve file info**

.. code:: python

    from openload import OpenLoad

    ol = OpenLoad('login', 'key')

    # Random file id.
    file_id = 'YMTqhQAuzVX'

    file_info = ol.file_info(file_id)
    print(file_info)

Documentation
-------------

documentation is available at https://pyopenload.readthedocs.io/.

.. _Openload.co: https://openload.co
.. _API: https://openload.co/api

.. |StarButton| image:: https://img.shields.io/github/stars/mohan3d/pyopenload.svg?style=social&label=Star&maxAge=3600
    :target: https://github.com/mohan3d/PyOpenload

.. |pypi| image:: https://img.shields.io/pypi/v/pyopenload.svg?maxAge=3600&style=flat-square
    :target: https://pypi.python.org/pypi/pyopenload

.. |format| image:: https://img.shields.io/pypi/format/pyopenload.svg?maxAge=3600&style=flat-square
    :target: https://pypi.python.org/pypi/pyopenload

.. |CodacyBadge| image:: https://img.shields.io/codacy/grade/42d0f198fcbe43daae71e21b6a3540fe.svg?maxAge=3600&style=flat-square
    :target: https://www.codacy.com/app/mohan3d94/PyOpenload?utm_source=github.com&utm_medium=referral&utm_content=mohan3d/PyOpenload&utm_campaign=badger

.. |license| image:: https://img.shields.io/pypi/l/pyopenload.svg?maxAge=3600&style=flat-square
    :target: https://choosealicense.com/licenses/mit/
    
.. |travis| image:: https://img.shields.io/travis/mohan3d/PyOpenload.svg?maxAge=3600&style=flat-square
    :target: https://travis-ci.org/mohan3d/PyOpenload

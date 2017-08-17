PyOpenload |StarButton|
=======================

python wrapper for `Openload.co`_ `API`_.

|Codacy Badge| |pypi| |format| |license|

Install
-------

.. code:: sh

    pip install pyopenload

Usage
-----

All methods return python dictionary

.. code:: python

    from openload import OpenLoad

    openload = OpenLoad('login', 'key')

    # User email
    account_info = openload.account_info()
    print(account_info['email'])

    # Download Ticket
    download_data = openload.prepare_download('file_id')
    print(download_data['ticket'])
    print(download_data['captcha_url'])
                         
    # Download Link
    download_url_data = openload.get_download_link('file_id', 'ticket', 'captcha_response')
    print(download_url_data['name'])
    print(download_url_data['url'])

    # Upload file
    openload.upload_file('file_path')
        

TODO
----

-  [ ] Tests

.. _Openload.co: https://openload.co
.. _API: https://openload.co/api

.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/42d0f198fcbe43daae71e21b6a3540fe
   :target: https://www.codacy.com/app/mohan3d94/PyOpenload?utm_source=github.com&utm_medium=referral&utm_content=mohan3d/PyOpenload&utm_campaign=badger

.. |StarButton| image:: https://img.shields.io/github/stars/mohan3d/pyopenload.svg?style=social&label=Star&maxAge=3600
   :target: https://github.com/mohan3d/PyOpenload

.. |pypi| image:: https://img.shields.io/pypi/v/pyopenload.svg?maxAge=3600&style=flat-square
   :target: https://pypi.python.org/pypi/pyopenload

.. |format| image:: https://img.shields.io/pypi/format/pyopenload.svg?maxAge=3600&style=flat-square
   :target: https://pypi.python.org/pypi/pyopenload

.. |license| image:: https://img.shields.io/pypi/l/pyopenload.svg?maxAge=3600&style=flat-square
   :target: https://choosealicense.com/licenses/mit/
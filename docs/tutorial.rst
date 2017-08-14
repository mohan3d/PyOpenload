========
Tutorial
========

Account
=======

Account Infos
-------------

.. code-block:: python
   :linenos:
   :emphasize-lines: 3,5

   def some_function():
       interesting = False
       print 'This line is highlighted.'
       print 'This one is not...'
       print '...but this one is.'
       
Get everything account related (total used storage, reward, ...).

.. code-block:: python
   :linenos:
   from __future__ import print_function

   from openload import OpenLoad

   # Find them in https://openload.co/account#usersettings
   username = 'FTP Username/API Login'
   key = 'FTP Password/API Key'

   openload = OpenLoad(username, key)
   info = openload.account_info()

   print(info)

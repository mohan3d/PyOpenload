========
Tutorial
========

:samp:`username` and :samp:`key` can be found in `openload user settings <https://openload.co/account#usersettings>`_.

Account
=======

Account Infos
-------------

Get everything account related (total used storage, reward, ...).

.. literalinclude:: ../examples/account_infos.py
   :linenos:

Download
========

Download Ticket
---------------

Generate a download token, will be used to generate direct download link.

.. literalinclude:: ../examples/download_ticket.py
   :linenos:

Download Link
-------------

Generate a download link, after generating a download ticket.

.. literalinclude:: ../examples/download_link.py
   :linenos:

Full example
------------

1) Generate a download token.
2) Solve captcha if needed.
3) Generate direct download url.

.. literalinclude:: ../examples/download_full.py
   :linenos:

File Info
---------

Check the status of a file (id, status, name, size, sha1, content_type).

.. literalinclude:: ../examples/file_info.py
   :linenos:
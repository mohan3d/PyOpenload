========
Examples
========

An instance of OpenLoad is needed for all examples.

.. literalinclude:: ../examples/base.py

:samp:`username` and :samp:`key` can be found in `openload user settings <https://openload.co/account#usersettings>`_.

Account
=======

Account Infos
-------------

Get everything account related (total used storage, reward, ...).

.. literalinclude:: ../examples/account_infos.py

   
Download
========

Download Ticket
---------------

Generate a download token, will be used to generate direct download link.

.. literalinclude:: ../examples/download_ticket.py

   
Download Link
-------------

Generate a download link, after generating a download ticket.

.. literalinclude:: ../examples/download_link.py

   
Full example
------------

1) Generate a download token.
2) Solve captcha if needed.
3) Generate direct download url.

.. literalinclude:: ../examples/download_full.py

   
File Info
---------

Check the status of a file (id, status, name, size, sha1, content_type).

.. literalinclude:: ../examples/file_info.py

   
Upload
======

Get an Upload URL
-----------------

You may need to use this method only if you want to re-implement :samp:`upload_file` in a different way.

Generate upload url, will be used to upload a file.

.. literalinclude:: ../examples/upload_link.py

   
Upload File
-----------

.. literalinclude:: ../examples/upload_link.py


Remote Upload
=============

Add Remote Upload
-----------------

Upload lastest pyopenload documentation pdf.

.. literalinclude:: ../examples/remote_upload.py


Check Remote Upload Status
--------------------------

Check the status of queued remote uploads.

.. literalinclude:: ../examples/check_remote_upload.py


File/Folder Management
======================

List Folder
-----------

List :samp:`Home` (The main directory).

.. literalinclude:: ../examples/list_folder.py


Rename Folder
-------------

Rename a specific folder.

.. literalinclude:: ../examples/rename_folder.py


Rename File
-----------

Rename a specific file.

.. literalinclude:: ../examples/rename_file.py


Delete File
-----------

Delete a specific file.

.. literalinclude:: ../examples/delete_file.py


Converting files
================

Convert a file
--------------

Convert previously uploaded file to a browser-streamable format :samp:`mp4 / h.264`

.. literalinclude:: ../examples/convert_file.py


Show running file converts
--------------------------

List all running conversions.

.. literalinclude:: ../examples/running_converts.py


Show failed file converts
-------------------------

Coming soon ... (Not yet implemented by openload.co API).


Get splash image
----------------

Get a download url of splash image for a specific uploaded file.

.. literalinclude:: ../examples/splash_image.py
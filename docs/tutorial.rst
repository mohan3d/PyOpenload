========
Tutorial
========

Download
========

PyOpenload doesn't download given file id, but gives us direct download url in two steps.

1) Generate a download token.
2) Get direct download url.

.. code-block:: python

    from __future__ import print_function

    from openload import OpenLoad

    # ----------- OpenLoad instance -----------
    username = 'FTP Username/API Login'
    key = 'FTP Password/API Key'

    ol = OpenLoad(username, key)

    # ------------- Generate token ------------
    file_id = 'Id of the file will be downloaded'

    # Get a download ticket and captcha url.
    preparation_resp = ol.prepare_download(file_id)
    ticket = preparation_resp.get('ticket')

    # Sometimes no captcha is sent in openload.co API response.
    captcha_url = preparation_resp.get('captcha_url')

    if captcha_url:
        # Solve captcha.
        captcha_response = solve_captcha(captcha_url)
    else:
        captcha_response = ''

    # --------- Get direct download url --------
    download_resp = ol.get_download_link(file_id, ticket, captcha_response)
    direct_download_url = download_resp.get('url')

    # Process download url.
    download(direct_download_url)

You must provide implementation of :samp:`solve_captcha` and :samp:`download` functions.


Extend
======

Upload large files
------------------

Large files (cannot fit into ram) can be uploaded using :samp:`requests-toolbelt MultipartEncoder`.

Install :samp:`requests-toolbelt`.

.. code-block:: bash

    $ pip install requests-toolbelt

.. code-block:: python

    from __future__ import print_function
    
    import os

    import requests
    from openload import OpenLoad
    from requests_toolbelt.multipart import encoder


    class MyOpenLoad(OpenLoad):
        def upload_large_file(self, file_path, **kwargs):  

            # Generate new upload url.     
            response = self.upload_link(**kwargs)
            upload_url = response['url']
                        
            upload_file = open(file_path, 'rb')        
            _, file_name = os.path.split(file_path)
            
            data = encoder.MultipartEncoder({
                "files": (file_name, upload_file, "application/octet-stream"),
            })
            
            headers = {"Prefer": "respond-async", "Content-Type": data.content_type}
            
            return requests.post(upload_url, headers=headers, data=data).json()
        

    ol = MyOpenLoad('login', 'key')
    uploaded_file_info = ol.upload_large_file('FILE_PATH')

    print(uploaded_file_info)


.. note:: 

    Upload large files code `contributed`_ by `playmusic9`_.


.. _contributed: https://github.com/mohan3d/PyOpenload/issues/5#issuecomment-325543121
.. _playmusic9: https://github.com/playmusic9
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
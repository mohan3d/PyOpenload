Quick-Start
===========

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
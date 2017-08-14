from __future__ import print_function

from openload import OpenLoad

username = 'FTP Username/API Login'
key = 'FTP Password/API Key'
file_id = 'Id of the file will be downloaded'
ticket = 'Ticket found in `prepare_download` response'
captcha_response = 'Solution of captcha found in `prepare_download` response'

openload = OpenLoad(username, key)
resp = openload.get_download_link(file_id,
                                  ticket,
                                  captcha_response)

direct_download_url = resp.get('url')

print(direct_download_url)

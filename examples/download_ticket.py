from __future__ import print_function

from openload import OpenLoad

username = 'FTP Username/API Login'
key = 'FTP Password/API Key'
file_id = 'Id of the file will be downloaded'

openload = OpenLoad(username, key)
resp = openload.prepare_download(file_id)

ticket = resp.get('ticket')
captcha_url = resp.get('captcha_url')

print(ticket)
print(captcha_url)
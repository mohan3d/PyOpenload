from __future__ import print_function

from openload import OpenLoad

username = 'FTP Username/API Login'
key = 'FTP Password/API Key'

openload = OpenLoad(username, key)
resp = openload.remote_upload_status()

print(resp)

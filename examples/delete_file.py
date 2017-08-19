from __future__ import print_function

from openload import OpenLoad

username = 'FTP Username/API Login'
key = 'FTP Password/API Key'
file_id = 'Id of the file will be deleted'

openload = OpenLoad(username, key)
resp = openload.delete_file(file_id)

print(resp)
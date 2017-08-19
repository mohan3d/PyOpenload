from __future__ import print_function

from openload import OpenLoad

username = 'FTP Username/API Login'
key = 'FTP Password/API Key'
file_id = 'Id of the file will be renamed'

openload = OpenLoad(username, key)
resp = openload.rename_file(file_id, '<NEW NAME>')

print(resp)

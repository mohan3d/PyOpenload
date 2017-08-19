from __future__ import print_function

from openload import OpenLoad

username = 'FTP Username/API Login'
key = 'FTP Password/API Key'
folder_id = 'Id of the folder will be renamed'

openload = OpenLoad(username, key)
resp = openload.rename_folder(folder_id, '<NEW NAME>')

print(resp)

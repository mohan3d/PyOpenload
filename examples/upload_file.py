from __future__ import print_function

from openload import OpenLoad

username = 'FTP Username/API Login'
key = 'FTP Password/API Key'
file_path = '/home/username/file.txt'

openload = OpenLoad(username, key)
resp = openload.upload_file(file_path)
uploaded_url = resp.get('url')

print(uploaded_url)

from __future__ import print_function

from openload import OpenLoad

username = 'FTP Username/API Login'
key = 'FTP Password/API Key'

pdf_url = 'https://media.readthedocs.org/pdf/pyopenload/latest/pyopenload.pdf'

openload = OpenLoad(username, key)
resp = openload.remote_upload(pdf_url)

file_id = resp.get('id')

print(file_id)

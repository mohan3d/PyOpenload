from __future__ import print_function
from pprint import pprint

from openload import OpenLoad

username = 'FTP Username/API Login'
key = 'FTP Password/API Key'
file_id = 'Id of the file will be downloaded'

openload = OpenLoad(username, key)
resp = openload.splash_image(file_id)

pprint(resp)
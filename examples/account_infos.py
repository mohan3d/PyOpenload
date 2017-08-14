from __future__ import print_function

from openload import OpenLoad

# Find them in https://openload.co/account#usersettings
username = 'FTP Username/API Login'
key = 'FTP Password/API Key'

openload = OpenLoad(username, key)
info = openload.account_info()

print(info)
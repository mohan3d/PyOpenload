from __future__ import print_function

from openload import OpenLoad


def solve_captcha(captcha_url):
    """Return solved captcha string"""
    pass

username = 'FTP Username/API Login'
key = 'FTP Password/API Key'
file_id = 'Id of the file will be downloaded'

openload = OpenLoad(username, key)

# Get a download ticket and captcha url.
preparation_resp = openload.prepare_download(file_id)
ticket = preparation_resp.get('ticket')

# Sometimes no captcha is sent in openload.co API response.
captcha_url = preparation_resp.get('captcha_url')

if captcha_url:
    # Solve captcha.
    captcha_response = solve_captcha(captcha_url)
else:
    captcha_response = ''

download_resp = openload.get_download_link(file_id, ticket, captcha_response)
direct_download_url = download_resp.get('url')

# Process download url.
print(direct_download_url)

file_id = 'Id of the file will be downloaded'

resp = ol.prepare_download(file_id)

ticket = resp.get('ticket')
captcha_url = resp.get('captcha_url')

print(ticket)
print(captcha_url)

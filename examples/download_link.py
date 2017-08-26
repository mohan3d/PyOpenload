file_id = 'Id of the file will be downloaded'
ticket = 'Ticket found in `prepare_download` response'
captcha_response = 'Solution of captcha found in `prepare_download` response'

resp = ol.get_download_link(file_id, ticket, captcha_response)
direct_download_url = resp.get('url')

print(direct_download_url)

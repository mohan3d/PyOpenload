pdf_url = 'https://media.readthedocs.org/pdf/pyopenload/latest/pyopenload.pdf'

resp = ol.remote_upload(pdf_url)
file_id = resp.get('id')

print(file_id)

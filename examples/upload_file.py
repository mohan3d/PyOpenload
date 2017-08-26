file_path = '/home/username/file.txt'

resp = ol.upload_file(file_path)
uploaded_url = resp.get('url')

print(uploaded_url)

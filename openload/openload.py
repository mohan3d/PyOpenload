import requests


class OpenLoad(object):
    api_base_url = 'https://api.openload.co/{api_version}/'
    api_version = '1'

    def __init__(self, api_login, api_key):
        self.login = api_login
        self.key = api_key
        self.api_url = self.api_base_url.format(api_version=self.api_version)
    
    def __get(self, url, params=None, logged_in=True, result_only=True):
        if not params:
            params = {}

        if logged_in:
            params.update({'login': self.login, 'key': self.key})

        response_json = requests.get(self.api_url + url, params).json()

        return response_json['result'] if result_only else response_json
    
    def account_info(self, result_only=True):
        return self.__get('account/info', result_only=result_only)

    def prepare_download(self, file_id, result_only=True):
        return self.__get('file/dlticket', params={'file': file_id}, result_only=result_only)

    def get_download_link(self, file_id, ticket, captcha_response=None):
        params = {'ticket': ticket, 'file': file_id}

        if captcha_response:
            params['captcha_response'] = captcha_response

        return self.__get('file/dl', params)

    def file_info(self, file_id, result_only=True):
        return self.__get('file/info', params={'file': file_id}, result_only=result_only)

    def upload_link(self, result_only=True, **kwargs):
        params = {key: value for key, value in kwargs.items() if value}
        return self.__get('file/ul', params=params, result_only=result_only)

    def upload_file(self, file_path, **kwargs):
        response = self.upload_link(**kwargs)
        upload_url = response['url']

        return requests.post(upload_url, files={'upload_file': open(file_path, 'rb')}).json()

    def remote_upload(self, remote_url, result_only=True, **kwargs):
        params = {'url': remote_url}
        params.update({key: value for key, value in kwargs.items() if value})

        return self.__get('remotedl/add', params=params, result_only=result_only)

    def remote_upload_status(self, result_only=True, **kwargs):
        params = {key: value for key, value in kwargs.items() if value}

        return self.__get('remotedl/status', params=params, result_only=result_only)

    def list_folder(self, folder_id=None, result_only=True):
        params = {'folder': folder_id} if folder_id else {}

        return self.__get('file/listfolder', params=params, result_only=result_only)

    def convert_file(self, file_id, result_only=True):
        return self.__get('file/convert', params={'file': file_id}, result_only=result_only)

    def running_conversions(self, folder_id=None, result_only=True):
        params = {'folder': folder_id} if folder_id else {}
        return self.__get('file/runningconverts', params=params, result_only=result_only)

    def failed_conversions(self):
        raise NotImplementedError

    def splash_image(self, file_id, result_only=True):
        return self.__get('file/getsplash', params={'file': file_id}, result_only=result_only)

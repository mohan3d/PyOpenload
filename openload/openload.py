import requests

from api_exceptions import (BadRequestException, BandwidthUsageExceeded,
                            FileNotFoundException, PermissionDeniedException,
                            ServerErrorException,
                            UnavailableForLegalReasonsException)


class OpenLoad(object):
    api_base_url = 'https://api.openload.co/{api_version}/'
    api_version = '1'

    def __init__(self, api_login, api_key):
        """Initializes OpenLoad instance with given parameters and formats api base url.

        Args:
            api_login (str): API Login found in openload.co
            api_key (str): API Key found in openload.co

        Returns:
            None
        """
        self.login = api_login
        self.key = api_key
        self.api_url = self.api_base_url.format(api_version=self.api_version)

    def __process_response(self, response_json, result_only=True):
        """Check of incoming response, raise error if it's needed otherwise return the incoming response_json

        Args:
            response_json (dict): results of the response of the GET request.
            result_only (bool): if it is true, only results are returned otherwise the whole response is returned.

        Returns:
            dict: results of the response of the GET request.
        """
        status = response_json['status']
        msg = response_json['msg']

        if status == 400:
            raise BadRequestException(msg)
        elif status == 403:
            raise PermissionDeniedException(msg)
        elif status == 404:
            raise FileNotFoundException(msg)
        elif status == 451:
            raise UnavailableForLegalReasonsException(msg)
        elif status == 509:
            raise BandwidthUsageExceeded(msg)
        elif status >= 500:
            raise ServerErrorException(msg)

        return response_json['result'] if result_only else response_json

    def __get(self, url, params=None, logged_in=True, result_only=True):
        """Used by every other method, it makes a GET request with the given params.

        Args:
            url (str): relative path of a specific service (account_info, prepare_download, .....).
            params (dict): contains parameters to be sent in the GET request.
            logged_in (bool): if it is true, use api_login/api_key otherwise don't use the (anonymous).
            result_only (bool): if it is true, only results are returned otherwise the whole response is returned.

        Returns:
            dict: results of the response of the GET request.

        """
        if not params:
            params = {}

        if logged_in:
            params.update({'login': self.login, 'key': self.key})

        response_json = requests.get(self.api_url + url, params).json()

        # return response_json['result'] if result_only else response_json
        return self.__process_response(response_json, result_only=result_only)

    def account_info(self, result_only=True):
        """Requests everything account related (total used storage, reward, ...).

        Args:
            result_only (bool): if it is true, only results are returned otherwise the whole response is returned.

        Returns:
            dict: dictionary containing response data of account_info request.
        """
        return self.__get('account/info', result_only=result_only)

    def prepare_download(self, file_id, result_only=True):
        """Makes a request to prepare for file download,
        this download preparation will be used before get_download_link method.

        Args:
            file_id (str): id of the file to be downloaded.
            say we have this url "https://openload.co/f/TJNMUk2hnYs/filename", TJNMUk2hnYs is the id of this file.

            result_only (bool): if it is true, only results are returned otherwise the whole response is returned.

        Returns:
            dict: dictionary containing response of prepare_download request.
        """
        return self.__get('file/dlticket', params={'file': file_id}, result_only=result_only)

    def get_download_link(self, file_id, ticket, captcha_response=None):
        """Requests direct download link for requested file,
        this method makes use of the response of prepare_download, prepare_download must be called first.

        Args:
            file_id (str): id of the file to be downloaded.

            ticket (str): preparation ticket is found in prepare_download response,
            this is why we need to call prepare_download before get_download_link.

            captcha_response (str): sometimes prepare_download will have captcha url to be solved first,
            this is the solution of the captcha.

        Returns:
            str: direct download link for the requested file.
        """
        params = {'ticket': ticket, 'file': file_id}

        if captcha_response:
            params['captcha_response'] = captcha_response

        return self.__get('file/dl', params)

    def file_info(self, file_id, result_only=True):
        """Used to request info for a specific file, info like size, name, .....

        Args:
            file_id (str): id of the file to be downloaded.
            result_only (bool): if it is true, only results are returned otherwise the whole response is returned.

        Returns:
            dict: dictionary containing response of file_info request.
        """
        return self.__get('file/info', params={'file': file_id}, result_only=result_only)

    def upload_link(self, result_only=True, **kwargs):
        """Makes a request to prepare for file upload.

        Args:
            result_only (bool): if it is true, only results are returned otherwise the whole response is returned.

            **kwargs: kwargs may contain (folder: Folder-ID to upload to,
                sha1: Expected sha1 If sha1 of uploaded file doesn't match this value upload fails,
                httponly: If this is set to true, use only http upload links).

        Returns:
            dict: dictionary containing response of upload_link request.
        """
        params = {key: value for key, value in kwargs.items() if value}
        return self.__get('file/ul', params=params, result_only=result_only)

    def upload_file(self, file_path, **kwargs):
        """Calls upload_link request to get valid url, then it makes a post request with given file to be uploaded.
        No need to call upload_link explicitly since upload_file calls it.

        Args:
            file_path (str): full path of the file to be uploaded.

            **kwargs: kwargs may contain (folder: Folder-ID to upload to,
                sha1: Expected sha1 If sha1 of uploaded file doesn't match this value upload fails,
                httponly: If this is set to true, use only http upload links).

        Returns:
            dict: dictionary containing response of upload_file request.
        """
        response = self.upload_link(**kwargs)
        upload_url = response['url']

        return requests.post(upload_url, files={'upload_file': open(file_path, 'rb')}).json()

    def remote_upload(self, remote_url, result_only=True, **kwargs):
        """Used to make a remote file upload to openload.co

        Args:
            remote_url (str): direct link of file to be remotely downloaded.
            result_only (bool): if it is true, only results are returned otherwise the whole response is returned.

            **kwargs: kwargs may contain (folder: Folder-ID to upload to,
                headers: additional HTTP headers, separated by newline (e.g. Cookies or HTTP Basic-Auth)).

        Returns:
            dict: dictionary containing response data of remote_upload request.

        """
        params = {'url': remote_url}
        params.update({key: value for key, value in kwargs.items() if value})

        return self.__get('remotedl/add', params=params, result_only=result_only)

    def remote_upload_status(self, result_only=True, **kwargs):
        """Checks a remote file upload to status.

        Args:
            result_only (bool): if it is true, only results are returned otherwise the whole response is returned.

            **kwargs: kwargs may contain (limit: Maximum number of results (Default: 5, Maximum: 100),
                id: Remote Upload ID)

        Returns:
            dict: dictionary containing response data of remote_upload_status request.

        """
        params = {key: value for key, value in kwargs.items() if value}

        return self.__get('remotedl/status', params=params, result_only=result_only)

    def list_folder(self, folder_id=None, result_only=True):
        """Request a list of files and folders in specified folder.

        Args:
            result_only (bool): if it is true, only results are returned otherwise the whole response is returned.
            folder_id (str): id of the folder to be listed.

        Returns:
            dict: dictionary containing response data of list_folder request.

        """
        params = {'folder': folder_id} if folder_id else {}

        return self.__get('file/listfolder', params=params, result_only=result_only)

    def convert_file(self, file_id, result_only=True):
        """Converts previously uploaded files to a browser-streamable format (mp4 / h.264).

        Args:
            file_id (str): id of the file to be converted.
            result_only (bool): if it is true, only results are returned otherwise the whole response is returned.

        Returns:
            dict: dictionary containing response data of convert_file request.

        """
        return self.__get('file/convert', params={'file': file_id}, result_only=result_only)

    def running_conversions(self, folder_id=None, result_only=True):
        """Shows running file converts by folder

        Args:
            folder_id (str): id of the folder to be listed, if not given root folder will be listed.
            result_only (bool): if it is true, only results are returned otherwise the whole response is returned.

        Returns:
            dict: dictionary containing response data of convert_file request.

        """
        params = {'folder': folder_id} if folder_id else {}
        return self.__get('file/runningconverts', params=params, result_only=result_only)

    def failed_conversions(self):
        """
        Not yet implemented, openload.co said "Coming soon ...".

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    def splash_image(self, file_id, result_only=True):
        """Shows the video splash image (thumbnail)

        Args:
            file_id (str): id of the target file.
            result_only (bool): if it is true, only results are returned otherwise the whole response is returned.

        Returns:
            dict: dictionary containing response data of splash_image request.
        """
        return self.__get('file/getsplash', params={'file': file_id}, result_only=result_only)

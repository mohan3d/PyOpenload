from __future__ import absolute_import

import os

import requests
import requests_toolbelt

from .api_exceptions import (BadRequestException, BandwidthUsageExceeded, FileNotFoundException,
                             PermissionDeniedException, TooManyRequestsException, ServerErrorException,
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

    @classmethod
    def _check_status(cls, response_json):
        """Check the status of the incoming response, raise exception if status is not 200.

        Args:
            response_json (dict): results of the response of the GET request.

        Returns:
           None

        """
        status = response_json['status']
        msg = response_json['msg']

        if status == 400:
            raise BadRequestException(msg)
        elif status == 403:
            raise PermissionDeniedException(msg)
        elif status == 404:
            raise FileNotFoundException(msg)
        elif status == 429:
            raise TooManyRequestsException(msg)
        elif status == 451:
            raise UnavailableForLegalReasonsException(msg)
        elif status == 509:
            raise BandwidthUsageExceeded(msg)
        elif status >= 500:
            raise ServerErrorException(msg)

    @classmethod
    def _process_response(cls, response_json):
        """Check the incoming response, raise error if it's needed otherwise return the incoming response_json

        Args:
            response_json (dict): results of the response of the GET request.

        Returns:
            dict: results of the response of the GET request.

        """

        cls._check_status(response_json)
        return response_json['result']

    def _get(self, url, params=None):
        """Used by every other method, it makes a GET request with the given params.

        Args:
            url (str): relative path of a specific service (account_info, ...).
            params (:obj:`dict`, optional): contains parameters to be sent in the GET request.

        Returns:
            dict: results of the response of the GET request.

        """
        if not params:
            params = {}

        params.update({'login': self.login, 'key': self.key})

        response_json = requests.get(self.api_url + url, params).json()

        return self._process_response(response_json)

    def account_info(self):
        """Requests everything account related (total used storage, reward, ...).

        Returns:
            dict: dictionary containing account related info. ::

                      {
                        "extid": "extuserid",
                        "email": "jeff@openload.io",
                        "signup_at": "2015-01-09 23:59:54",
                        "storage_left": -1,
                        "storage_used": "32922117680",
                        "traffic": {
                          "left": -1,
                          "used_24h": 0
                        },
                        "balance": 0
                      }

        """
        return self._get('account/info')

    def prepare_download(self, file_id):
        """Makes a request to prepare for file download,
        this download preparation will be used before get_download_link method.

        Args:
            file_id (str): id of the file to be downloaded.

        Returns:
            dict: dictionary containing (ticket, captcha info, ...). ::

                  {
                    "ticket": "72fA-_Lq8Ak~~1440353112~n~~0~nXtN3RI-nsEa28Iq",
                    "captcha_url": "https://openload.co/dlcaptcha/b92eY_nfjV4.png",
                    "captcha_w": 140,
                    "captcha_h": 70,
                    "wait_time": 10,
                    "valid_until": "2015-08-23 18:20:13"
                 }

        """
        return self._get('file/dlticket', params={'file': file_id})

    def get_download_link(self, file_id, ticket, captcha_response=None):
        """Requests direct download link for requested file,
        this method makes use of the response of prepare_download, prepare_download must be called first.

        Args:
            file_id (str): id of the file to be downloaded.

            ticket (str): preparation ticket is found in prepare_download response,\
                          this is why we need to call prepare_download before get_download_link.

            captcha_response (:obj:`str`, optional): sometimes prepare_download will have captcha url to be solved, \
                                                     first, this is the solution of the captcha.

        Returns:
            dict: dictionary containing (file info, download url, ...). ::

                  {
                    "name": "The quick brown fox.txt",
                    "size": 12345,
                    "sha1": "2fd4e1c67a2d28fced849ee1bb76e7391b93eb12",
                    "content_type": "plain/text",
                    "upload_at": "2011-01-26 13:33:37",
                    "url": "https://abvzps.example.com/dl/l/4spxX_-cSO4/The+quick+brown+fox.txt",
                    "token": "4spxX_-cSO4"
                  }

        """
        params = {'ticket': ticket, 'file': file_id}

        if captcha_response:
            params['captcha_response'] = captcha_response

        return self._get('file/dl', params)

    def file_info(self, file_id):
        """Used to request info for a specific file, info like size, name, .....

        Args:
            file_id (str): File-ID(s), single file or comma-separated (max. 50)

        Returns:
            dict: dictionary containing file(s) info, each key represents a file_id. ::

                  {
                     "72fA-_Lq8Ak3": {
                        "id": "72fA-_Lq8Ak3",
                        "status": 200,
                        "name": "The quick brown fox.txt",
                        "size": 123456789012,
                        "sha1": "2fd4e1c67a2d28fced849ee1bb76e7391b93eb12",
                        "content_type": "plain/text",
                     },
                     "72fA-_Lq8Ak4": {
                        "id": "72fA-_Lq8Ak4",
                        "status": 500,
                        "name": "The quick brown fox.txt",
                        "size": false,
                        "sha1": "2fd4e1c67a2d28fced849ee1bb76e7391b93eb12",
                        "content_type": "plain/text",
                     },
                     ...
                   }

        """
        return self._get('file/info', params={'file': file_id})

    def upload_link(self, folder_id=None, sha1=None, httponly=False):
        """Makes a request to prepare for file upload.

        Note:
            If folder_id is not provided, it will make and upload link to the ``Home`` folder.

        Args:
            folder_id (:obj:`str`, optional): folder-ID to upload to.
            sha1 (:obj:`str`, optional): expected sha1 If sha1 of uploaded file doesn't match this value, upload fails.
            httponly (:obj:`bool`, optional): If this is set to true, use only http upload links.

        Returns:
            dict: dictionary containing (url: will be used in actual upload, valid_until). ::

                {
                    "url": "https://1fiafqj.oloadcdn.net/uls/nZ8H3X9e0AotInbU",
                    "valid_until": "2017-08-19 19:06:46"
                }

        """

        kwargs = {'folder': folder_id, 'sha1': sha1, 'httponly': httponly}
        params = {key: value for key, value in kwargs.items() if value}
        return self._get('file/ul', params=params)

    def upload_file(self, file_path, folder_id=None, sha1=None, httponly=False):
        """Calls upload_link request to get valid url, then it makes a post request with given file to be uploaded.
        No need to call upload_link explicitly since upload_file calls it.

        Note:
            If folder_id is not provided, the file will be uploaded to ``Home`` folder.

        Args:
            file_path (str): full path of the file to be uploaded.
            folder_id (:obj:`str`, optional): folder-ID to upload to.
            sha1 (:obj:`str`, optional): expected sha1 If sha1 of uploaded file doesn't match this value, upload fails.
            httponly (:obj:`bool`, optional): If this is set to true, use only http upload links.

        Returns:
            dict: dictionary containing uploaded file info. ::

                {
                    "content_type": "application/zip",
                    "id": "0yiQTPzi4Y4",
                    "name": 'favicons.zip',
                    "sha1": 'f2cb05663563ec1b7e75dbcd5b96d523cb78d80c',
                    "size": '24160',
                    "url": 'https://openload.co/f/0yiQTPzi4Y4/favicons.zip'
                 }

        """

        upload_url_response_json = self.upload_link(folder_id=folder_id, sha1=sha1, httponly=httponly)
        upload_url = upload_url_response_json['url']

        _, file_name = os.path.split(file_path)

        with open(file_path, 'rb') as f:
            data = requests_toolbelt.MultipartEncoder({
                "files": (file_name, f, "application/octet-stream"),
            })

            headers = {"Content-Type": data.content_type}
            response_json = requests.post(upload_url, data=data, headers=headers).json()

        self._check_status(response_json)
        return response_json['result']

    def remote_upload(self, remote_url, folder_id=None, headers=None):
        """Used to make a remote file upload to openload.co

        Note:
            If folder_id is not provided, the file will be uploaded to ``Home`` folder.

        Args:
            remote_url (str): direct link of file to be remotely downloaded.
            folder_id (:obj:`str`, optional): folder-ID to upload to.
            headers (:obj:`dict`, optional): additional HTTP headers (e.g. Cookies or HTTP Basic-Auth)

        Returns:
            dict: dictionary containing ("id": uploaded file id, "folderid"). ::

                {
                    "id": "12",
                    "folderid": "4248"
                }

        """

        kwargs = {'folder': folder_id, 'headers': headers}
        params = {'url': remote_url}
        params.update({key: value for key, value in kwargs.items() if value})

        return self._get('remotedl/add', params=params)

    def remote_upload_status(self, limit=None, remote_upload_id=None):
        """Checks a remote file upload to status.

        Args:
            limit (:obj:`int`, optional): Maximum number of results (Default: 5, Maximum: 100).
            remote_upload_id (:obj:`str`, optional): Remote Upload ID.

        Returns:
            dict: dictionary containing all remote uploads, each dictionary element is a dictionary. ::

                {
                    "24": {
                      "id": "24",
                      "remoteurl": "http://proof.ovh.net/files/100Mio.dat",
                      "status": "new",
                      "folderid": "4248",
                      "added": "2015-02-21 09:20:26",
                      "last_update": "2015-02-21 09:20:26",
                      "extid": False,
                      "url": False
                    },
                    "22": {
                      "id": "22",
                      "remoteurl": "http://proof.ovh.net/files/1Gio.dat",
                      "status": "downloading",
                      "bytes_loaded": "823997062",
                      "bytes_total": "1073741824",
                      "folderid": "4248",
                      "added": "2015-02-21 09:20:26",
                      "last_update": "2015-02-21 09:21:56",
                      "extid": False,
                      "url": False
                    },
                    ...
                }

        """

        kwargs = {'limit': limit, 'id': remote_upload_id}
        params = {key: value for key, value in kwargs.items() if value}

        return self._get('remotedl/status', params=params)

    def list_folder(self, folder_id=None):
        """Request a list of files and folders in specified folder.

        Note:
            if folder_id is not provided, ``Home`` folder will be listed

        Args:
            folder_id (:obj:`str`, optional): id of the folder to be listed.

        Returns:
            dict: dictionary containing only two keys ("folders", "files"), \
                  each key represents a list of dictionaries. ::

                      {
                        "folders": [
                          {
                            "id": "5144",
                            "name": ".videothumb"
                          },
                          {
                            "id": "5792",
                            "name": ".subtitles"
                          },
                          ...
                        ],
                        "files": [
                          {
                            "name": "big_buck_bunny.mp4.mp4",
                            "sha1": "c6531f5ce9669d6547023d92aea4805b7c45d133",
                            "folderid": "4258",
                            "upload_at": "1419791256",
                            "status": "active",
                            "size": "5114011",
                            "content_type": "video/mp4",
                            "download_count": "48",
                            "cstatus": "ok",
                            "link": "https://openload.co/f/UPPjeAk--30/big_buck_bunny.mp4.mp4",
                            "linkextid": "UPPjeAk--30"
                          },
                          ...
                        ]
                      }

        """
        params = {'folder': folder_id} if folder_id else {}

        return self._get('file/listfolder', params=params)

    def rename_folder(self, folder_id, name):
        """Sets a new name for a folders

        Note:
            folder_id(s) can be found in list_folder return.

        Args:
            folder_id (str): id of the folder to be renamed.
            name (str): new name for the provided folder.

        Returns:
            bool: True if folder is renamed, otherwise False.

        """
        return self._get('file/renamefolder', params={'folder': folder_id, 'name': name})

    def rename_file(self, file_id, name):
        """Sets a new name for a file

        Args:
            file_id (str): id of the file to be renamed.
            name (str): new name for the provided file.

        Returns:
            bool: True if file is renamed, otherwise False.

        """
        return self._get('file/rename', params={'file': file_id, 'name': name})

    def delete_file(self, file_id):
        """Removes one of your files

        Args:
            file_id (str): id of the file to be deleted.

        Returns:
            bool: True if file is deleted, otherwise False.

        """
        return self._get('file/delete', params={'file': file_id})

    def convert_file(self, file_id):
        """Converts previously uploaded files to a browser-streamable format (mp4 / h.264).

        Args:
            file_id (str): id of the file to be converted.

        Returns:
            bool: True if conversion started, otherwise False.

        """
        return self._get('file/convert', params={'file': file_id})

    def running_conversions(self, folder_id=None):
        """Shows running file converts by folder

        Note:
            If folder_id is not provided, ``Home`` folder will be used.

        Args:
            folder_id (:obj:`str`, optional): id of the folder to list conversions of files exist in it.

        Returns:
            list: list of dictionaries, each dictionary represents a file conversion info. ::

                      [
                        {
                          "name": "Geysir.AVI",
                          "id": "3565411",
                          "status": "pending",
                          "last_update": "2015-08-23 19:41:40",
                          "progress": 0.32,
                          "retries": "0",
                          "link": "https://openload.co/f/f02JFG293J8/Geysir.AVI",
                          "linkextid": "f02JFG293J8"
                        },
                        ....
                      ]

        """
        params = {'folder': folder_id} if folder_id else {}
        return self._get('file/runningconverts', params=params)

    def failed_conversions(self):
        """
        Not yet implemented, openload.co said "Coming soon ...".

        Raises:
            NotImplementedError

        """
        raise NotImplementedError

    def splash_image(self, file_id):
        """Shows the video splash image (thumbnail)

        Args:
            file_id (str): id of the target file.

        Returns:
            str: url for the splash image.

        """
        return self._get('file/getsplash', params={'file': file_id})

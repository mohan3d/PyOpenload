import os
import unittest

import openload


class TestOpenLoad(unittest.TestCase):
    def setUp(self):
        login = os.environ.get('OPENLOAD_LOGIN')
        key = os.environ.get('OPENLOAD_KEY')

        self.ol = openload.OpenLoad(login, key)

        self.file_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'file.txt')

        self.uploaded_files_ids = []

    def tearDown(self):
        file_ids = self.uploaded_files_ids

        if file_ids:
            self.delete_test_files(file_ids)

    def delete_test_files(self, ids):
        for file_id in ids:
            self.ol.delete_file(file_id)

    def get_folder_id(self):
        home_folder_info = self.ol.list_folder()
        folders = home_folder_info.get('folders')

        if folders:
            return folders[-1].get('id')

    def test_account_info(self):
        account_info = self.ol.account_info()
        keys = ['balance', 'email', 'extid', 'signup_at', 'storage_left', 'storage_used', 'traffic']

        self.assertIsInstance(account_info, dict)

        for key in keys:
            self.assertIn(key, account_info)

    def test_upload_link(self):
        upload_link_info = self.ol.upload_link()

        self.assertIsInstance(upload_link_info, dict)
        self.assertIn('url', upload_link_info)
        self.assertIn('valid_until', upload_link_info)

    def test_upload_file_without_folder(self):
        file_info = self.ol.upload_file(self.file_path)
        keys = ['content_type', 'id', 'name', 'sha1', 'size', 'url']

        self.uploaded_files_ids.append(file_info.get('id'))

        self.assertIsInstance(file_info, dict)

        for key in keys:
            self.assertIn(key, file_info)

    def test_upload_file_with_folder(self):
        folder_id = self.get_folder_id()
        file_info = self.ol.upload_file(self.file_path, folder_id=folder_id)
        keys = ['content_type', 'id', 'name', 'sha1', 'size', 'url']

        self.uploaded_files_ids.append(file_info.get('id'))

        self.assertIsInstance(file_info, dict)

        for key in keys:
            self.assertIn(key, file_info)

        self.uploaded_files_ids.append(file_info.get('id'))

    def test_file_info_single_file(self):
        uploaded_file_info = self.ol.upload_file(self.file_path)
        file_id = uploaded_file_info.get('id')

        self.uploaded_files_ids.append(file_id)

        file_info = self.ol.file_info(file_id)

        self.assertIsInstance(file_info, dict)
        self.assertIn(file_id, file_info)
        self.assertIsInstance(file_info.get(file_id), dict)

    def test_file_info_multiple_files(self):
        uploaded_files_info = [self.ol.upload_file(self.file_path),
                               self.ol.upload_file(self.file_path),
                               self.ol.upload_file(self.file_path)]

        files_ids = [info.get('id') for info in uploaded_files_info]
        self.uploaded_files_ids.extend([file_id for file_id in files_ids if file_id])

        self.assertTrue(all(files_ids))

        files_info = self.ol.file_info(','.join(files_ids))

        for file_id, file_info in files_info.items():
            self.assertIsInstance(file_info, dict)
            self.assertIn(file_id, files_info)
            self.assertIsInstance(files_info.get(file_id), dict)

    def test_prepare_download(self):
        file_info = self.ol.upload_file(self.file_path)
        file_id = file_info.get('id')
        keys = ["ticket", "captcha_url", "captcha_w", "captcha_h", "wait_time", "valid_until"]

        self.uploaded_files_ids.append(file_id)

        prepare_info = self.ol.prepare_download(file_id)

        self.assertIsInstance(prepare_info, dict)

        for key in keys:
            self.assertIn(key, prepare_info)

    def test_list_folder_without_folder(self):
        folder_info = self.ol.list_folder()

        self.assertIsInstance(folder_info, dict)
        self.assertIn('folders', folder_info)
        self.assertIn('files', folder_info)

    def test_list_folder_with_folder(self):
        folder_id = self.get_folder_id()
        folder_info = self.ol.list_folder(folder_id)

        self.assertIsInstance(folder_info, dict)
        self.assertIn('folders', folder_info)
        self.assertIn('files', folder_info)

    def test_rename_file(self):
        file_info = self.ol.upload_file(self.file_path)
        file_id = file_info.get('id')
        self.uploaded_files_ids.append(file_id)

        succeeded = self.ol.rename_file(file_id, 'NEW_NAME')
        self.assertTrue(succeeded)

    def test_delete_file(self):
        file_info = self.ol.upload_file(self.file_path)
        file_id = file_info.get('id')

        succeeded = self.ol.delete_file(file_id)
        self.assertTrue(succeeded)

    def test_running_conversions_without_folder(self):
        conversions = self.ol.running_conversions()
        self.assertIsInstance(conversions, list)

    def test_running_conversions_with_folder(self):
        folder_id = self.get_folder_id()
        conversions = self.ol.running_conversions(folder_id=folder_id)
        self.assertIsInstance(conversions, list)

    def test_remote_upload_status(self):
        remote_upload_status_info = self.ol.remote_upload_status()
        self.assertIsInstance(remote_upload_status_info, dict)


if __name__ == '__main__':
    unittest.main()

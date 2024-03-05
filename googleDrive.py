from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import re


class GDrive:
    def __init__(self, credentials_file=""):
        if credentials_file == "":
            dir = os.path.dirname(__file__)
            files = os.listdir(dir)
            if "client_secrets.json" in files:
                self.credentials_file = os.path.join(dir, "client_secrets.json")
        else:
            self.credentials_file = credentials_file
        self.drive = self._authenticate()

    def _authenticate(self):
        """
        Authenticate the client to Google Drive and return an instance of Google Drive
        """
        gauth = GoogleAuth()
        gauth.DEFAULT_SETTINGS['client_config_file'] = self.credentials_file
        gauth.LocalWebserverAuth()
        return GoogleDrive(gauth)
    
    def _getFile(self, id):
        """
        Get a Google Drive file using its id
        """
        return self.drive.CreateFile({'id': id})
    
    def _getFile(self, folder_id, filename):
        """
        Get the first Google Drive file matching the filename inside a folder.
        """
        return self._getFiles(folder_id, filename)[0]
    
    def _getFiles(self, folder_id, filename, partial=False):
        """
        Get all Google Drive files matching the filename inside a folder.
        """
        if partial:
            query = "'{}' in parents and trashed=false and title contains '{}'".format(folder_id, filename)
        else:
            query = "'{}' in parents and trashed=false and title='{}'".format(folder_id, filename)
        return self.drive.ListFile({'q': query}).GetList()
    
    def _getNextVersionFilename(self, folder_id, filename):
        """
        Checks a Google Drive folder for any existing file containing the filename with a version number suffix,
        then increment the version number and return the filename
        """
        name, extension = os.path.splitext(filename)
        gfiles = self._getFiles(folder_id=folder_id, filename=name, partial=True)
        count = 0
        if len(gfiles) > 0:
            # check if our versioning suffix is found (ex: "_v999")
            pattern = r'_v\d{3}'
            for file in gfiles:
                if re.search(pattern, file['title']):
                    count += 1

        return "{}_v{:03d}{}".format(name, count + 1, extension)

    def Upload(self, filepath, folder_id="", mode=0):
        """
        Upload a file to a Google Drive folder
        :param folder_id: Destination folder ID, this can be found on Google Drive URL while browsing. Default to root folder.
        :param mode: Upload mode, 0 = versioning using a filename suffix "_v999",  1 = overwrite existing file.
        """
        if not os.path.isfile(filepath):
            raise FileNotFoundError("Error: file does not exist: {}".format(filepath))
        
        filename = filepath.split("/")[-1]
        meta = {}
        if folder_id != "":
            meta['parents'] = [{'id': folder_id}]
        
        out = None

        # Versioning Mode
        if mode == 0:
            filename = self._getNextVersionFilename(folder_id, filename)
        # Overwrite mode
        elif mode == 1:
            out = self._getFile(folder_id, filename)
            if out['id'] is not None:
                meta['id'] = out['id']
        
        meta['title'] = filename
        
        gfile = self.drive.CreateFile(meta)
        gfile.SetContentFile(filepath)
        gfile.Upload()
        return gfile

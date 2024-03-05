import hou

class GDriveSave:
    """
    Save to Google Drive HDA 
    """
    def __init__(self, node_hda):
        self.node_hda = node_hda
        

    def CreateFileCache(self, node_cache):
        """
        Use a file cache node to create the file to be saved on Google Drive
        """
        self.node_cache = node_cache
        import os
        
        filename = self.node_hda.parm("filename").eval()
        cache_path = self.node_hda.parm("cache_path").eval()
        if not filename:
            print("Error: Filename cannot be empty")
        elif not cache_path:
            print("Error: Cache Path cannot be empty")
        
        ext_idx = self.node_hda.parm("extension").evalAsInt()
        filename = "{}.{}".format(filename, self.node_hda.parm("extension").menuLabels()[ext_idx])
        path = os.path.join(cache_path,filename).replace("\\", "/")

        self.node_cache.parm("file").set(path)
        self.node_cache.parm("execute").pressButton()

    def UploadToGDrive(self):
        """
        Called after the cache file has been created
        """
        import googleDrive
        gdrive = googleDrive.GDrive()
        filepath = self.node_cache.parm("file").eval()
        folder_id = self.node_hda.parm("folder_id").eval()
        mode = self.node_hda.parm("mode").eval()
        gfile = gdrive.Upload(filepath, folder_id, mode)
        
        # Show the newly uploaded file uri
        self.node_hda.parm("uploaded_file").set(gfile['alternateLink'])

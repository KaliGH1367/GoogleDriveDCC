import sys
import os
import hou
import houGoogleDrive

# Google Drive DCC
gddcc_path = os.environ.get("GOOGLE_DRIVE_DCC")
if gddcc_path not in sys.path:
    sys.path.append(gddcc_path)

# Houdini Google Drive
hougdrive = gddcc_path + "/Houdini/python3.10libs"
if hougdrive not in sys.path:
    sys.path.append(hougdrive)

# Conda Environment
conda_path = "C:/Users/faz02/miniconda3/envs/GoogleDriveDCC/Lib/site-packages"
if conda_path not in sys.path:
    sys.path.append(conda_path)

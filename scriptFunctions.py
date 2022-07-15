from library import settings
from pathlib import Path
from library.download import downloadFile

import os, shutil, subprocess

try:
    import requests
except ModuleNotFoundError:
    subprocess.run(["pip install requests"])

import os
from pathlib import Path
from datetime import datetime


class Log:
    _instance = None

    def __init__(self):
        self.fileName = str(datetime.now())
        self.fullPath = self._getFullPath()
        self.message = ""

    def __new__(cls, *args, **kwargs):  # creates a singleton pattern
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _getFullPath(self):
        now = datetime.now()

        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../Output/' + self.fileName + ".txt")
        return filename

    def log(self, msg):
        self.message += msg
        self.message += "\n"

    def save(self):
        with open(self.fullPath, 'w') as file:  # relative path is not working.

            file.write(self.message)

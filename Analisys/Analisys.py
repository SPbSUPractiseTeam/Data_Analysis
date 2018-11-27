from .video import main as m1
from .tests import main as m2
import sqlite3

_modules = [m1, m2]

_database = None
_cursor = None
_courseName = None

def SetData(databaseName):
    global _cursor, _database, _courseName
    _database = sqlite3.connect(databaseName)
    _courseName = databaseName.split('.')[0]
    _cursor = _database.cursor()

def UseModule(id):
    global _cursor, _courseName, _modules
    if id >= len(_modules):
        return None
    else:
        return _modules[id].Execute(_cursor, _courseName)

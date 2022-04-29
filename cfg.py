# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from decouple import RepositoryIni, Config

config = Config(RepositoryIni('setting.ini'))

CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = config('SPOTIPY_REDIRECT_URI')
DB_CONNSTR = config('DB_CONNSTR')
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 18:29:24 2022

@author: josee
"""

import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db
import sqlite3

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost:8888/callback",
    scope="user-read-recently-played"))

def extract (date, limit = 50):
    ds = int(date.timestamp()) * 1000
    return sp.current_user_recently_played(limit = limit, after = ds)

def transform(raw_data, date):
    data = []
    for r in raw_data['items']:
        data.append(
            {
                'played_at': r['played_at'],
                'artist': r['track']['artists'][0]['name'],
                'track': r['track']['name'],
                'explicit': r['track']['explicit'],
                'duration_ms': r['track']['duration_ms'] 
            }
        )
    df = pd.DataFrame(data)
    clean_df = df[pd.to_datetime(df['played_at']).dt.date == datetime.today().date()]
    return clean_df

def load(clean_df):
    DATABASE_LOCATION = 'sqlite:///played_tracks.sqlite'
    engine = db.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('played_tracks.sqlite')
    cursor = conn.cursor()
    query = '''CREATE TABLE IF NOT EXISTS played_tracks(
            played_at VARCHAR(200),
            artist VARCHAR(200),
            track VARCHAR (200),
            explicit VARCHAR (200),
            duration_ms VARCHAR (200),
            CONSTRAINT primary_key_contraint PRIMARY KEY (played_at)
        ) '''
    cursor.execute(query)
    clean_df.to_sql('played_tracks', engine, index = False, if_exists= 'append')
    conn.close()

if __name__ == '__main__':
    date = datetime.today() - timedelta(days = 1)
    
    #EXTRACT
    data_raw = extract(date)
    print(f"Extracted {len(data_raw['items'])} registers")
    #TRANSFORM
    clean_df = transform (data_raw, date)
    print(f"{clean_df.shape[0]} registers after transform")
    #LOAD
    load(clean_df)
    print('Data loaded to database')

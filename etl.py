import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from datetime import datetime
import sys


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values
    for song in song_data:
        cur.execute(song_table_insert, song)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values
    for artist in artist_data:
        cur.execute(artist_table_insert, artist)


def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.query("page=='NextSong'")

    # insert time data records
    time_data = []
    for i, t in df.iterrows():
        dt = datetime.fromtimestamp(t['ts']/1000)
        time_data.append([dt, dt.hour, dt.day, dt.date().isocalendar()[1], dt.month, dt.year, dt.weekday()])

    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(time_data, columns=column_labels)

    cur.execute("DELETE FROM time;")

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    user_df.rename(columns={'userId': 'user_id', 'firstName': 'first_name', 'lastName': 'last_name'})

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    cur.execute("DELETE FROM songplays;")

    # insert songplay records
    for index, row in df.iterrows():
        start_time = datetime.fromtimestamp(t['ts']/1000)

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [start_time, row['userId'], row['level'], songid, artistid, row['sessionId'], row['location'],
                         row['userAgent']]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=postgres dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()

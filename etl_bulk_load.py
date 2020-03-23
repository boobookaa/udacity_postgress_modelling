import os
import glob
import psycopg2
import pandas as pd
from datetime import datetime
from sql_queries import *


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(path_or_buf = filepath, typ = 'series')

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].tolist()
    cur.execute(artist_table_insert, artist_data)

def process_log_file(cur, filepath):
    # open log file and format it to the correct json structure
    with open(filepath, 'r') as f:
        data = (line.strip() for line in f)
        data_json = "[{0}]".format(','.join(data))
    df = pd.read_json(data_json)

    # filter by NextSong action
    df = df.query("page == 'NextSong'")

    # convert timestamp column to datetime
    df.insert(len(df.columns), column='ts_ds', value = pd.to_datetime(df['ts'], unit = 'ms'))
    df = df.rename(columns = { 'ts':'ts_src', 'ts_ds':'ts'}, inplace = False)

    t = df['ts']
    
    # insert time data records
    time_data = (t, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table and remove duplicates rows
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']].query("userId != '' and userId != 'None'").copy()
    user_df.drop_duplicates(keep = 'last', inplace = True)

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # clear data: userId is 'int' in the tables and can be either 'str' or 'number' in the dataframe. 
    # So it must be an error due to '' values while formating a query
    if df['userId'].dtypes == 'object':
        df['userId'] = df['userId'].replace({'': None})

    df.insert(len(df.columns), column='filepath', value = filepath)

    # write data to the CSV file. File is opened in append mode
    df.to_csv('data/log_data/log_data_file.csv', sep = '|', index = False, quotechar = '"', mode = 'a', header = False, 
              columns = ['ts', 'userId', 'artist', 'song', 'length', 'level', 'sessionId', 'location', 
                         'userAgent', 'filepath'])

#    cur.execute(songplay_table_insert, songplay_data)

def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        print('------ Start processing: ' + datafile)
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed'.format(i, num_files))

def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    
    # truncate stage table for sonplays
    cur.execute(stg_songplay_table_truncate)
    
    # delete csv file with old data
    try:
        os.remove('data/log_data/log_data_file.csv')
    except OSError as error: 
        print('log_data_file does not exists')
    
    # process_data into csv file
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)
    
    # copy data from csv file to table at the stg layer. And then merge data into the main table
    cur.execute(stg_songplay_table_copy)
    print('{} rows were processed from log_data_file.csv to stg_songplays table'.format(cur.rowcount))
    cur.execute(songplay_table_merge)
    print('{} rows were processed from stage layer to songplays table'.format(cur.rowcount))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
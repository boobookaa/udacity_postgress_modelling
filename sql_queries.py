# DROP TABLES

songplay_table_drop = "drop table if exists songplays;"
user_table_drop = "drop table if exists users;"
song_table_drop = "drop table if exists songs;"
artist_table_drop = "drop table if exists artists;"
time_table_drop = "drop table if exists time;"
stg_songplay_table_drop = "drop table if exists stg_songplays;"


# CREATE TABLES

songplay_table_create = ("create table if not exists songplays (\
    songplay_id serial primary key,\
    start_time timestamp,\
    user_id int,\
    level varchar,\
    song_id varchar,\
    artist_id varchar,\
    session_id int,\
    location varchar,\
    user_agent varchar,\
    constraint unq_songplays unique(start_time, user_id, song_id, session_id));")

stg_songplay_table_create = ("create unlogged table if not exists stg_songplays (\
    ts timestamp,\
    userid varchar,\
    artist varchar,\
    song varchar,\
    length float,\
    level varchar,\
    sessionid int,\
    location varchar,\
    useragent varchar,\
    filepath varchar);")

user_table_create = ("create table if not exists users (\
    user_id int primary key,\
    first_name varchar,\
    last_name varchar,\
    gender char(1),\
    level varchar);")

song_table_create = ("create table if not exists songs (\
    song_id varchar primary key,\
    title varchar,\
    artist_id varchar,\
    year int,\
    duration float);")

artist_table_create = ("create table if not exists artists (\
    artist_id varchar primary key,\
    name varchar,\
    location varchar,\
    latitude varchar(20),\
    longitude varchar(20));")

time_table_create = ("create table if not exists time (\
    start_time timestamp primary key,\
    hour smallint,\
    day smallint,\
    week smallint,\
    month smallint,\
    year smallint,\
    weekday varchar);")


# INSERT RECORDS

songplay_table_insert = ("insert into songplays (start_time, user_id, level, song_id, artist_id, \
    session_id, location, user_agent) values(%s, %s, %s, %s, %s, %s, %s, %s);")

stg_songplay_table_insert = ("insert into songplays (start_time, user_id, level, song_id, artist_id, \
    session_id, location, user_agent, filepath) values(%s, %s, %s, %s, %s, %s, %s, %s, %s);")

user_table_insert = ("insert into users (user_id, first_name, last_name, gender, level) values(%s, %s, %s, %s, %s) \
    on conflict (user_id) do nothing;")

song_table_insert = ("insert into songs (song_id, title, artist_id, year, duration) values (%s, %s, %s, %s, %s) \
    on conflict (song_id) do nothing;")

artist_table_insert = ("insert into artists (artist_id, name, location, latitude, longitude) values(%s, %s, %s, %s, %s) \
    on conflict (artist_id) do nothing;")

time_table_insert = ("insert into time (start_time, hour, day, week, month, year, weekday) \
    values(%s, %s, %s, %s, %s, %s, %s) \
    on conflict (start_time) do nothing;")


# FIND SONGS

song_select = ("select s.song_id, a.artist_id \
    from songs s \
    inner join artists a on s.artist_id = a.artist_id \
    where s.title =  %(song)s and s.duration = %(length)s and a.name = %(artist)s;")


# TRUNCATE TABLES

stg_songplay_table_truncate = "truncate table stg_songplays;"

# BULK LOAD AND MERGES

stg_songplay_table_copy = "copy stg_songplays (ts, userid, artist, song, length, level, sessionid, location, \
    useragent, filepath) from '/home/workspace/data/log_data/log_data_file.csv' with delimiter '|' csv;"

songplay_table_merge = "insert into songplays (start_time, user_id, level, song_id, artist_id, session_id, \
    location, user_agent) \
    with artist_song as \
    ( \
        select s.song_id \
            , a.artist_id \
            , s.title \
            , s.duration \
            , a.name \
        from songs s \
        inner join artists a on s.artist_id = a.artist_id \
    ) \
        select ssp.ts as start_time\
            , cast(ssp.userid as int) as user_id\
            , ssp.level\
            , artist_song.song_id\
            , artist_song.artist_id\
            , ssp.sessionid as session_id\
            , ssp.location\
            , ssp.useragent as user_agent\
        from stg_songplays ssp\
        left join artist_song on ssp.song = artist_song.title\
            and ssp.length = artist_song.duration \
            and ssp.artist = artist_song.name\
        on conflict do nothing;"

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, 
                        time_table_create, stg_songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop, 
                      stg_songplay_table_drop]

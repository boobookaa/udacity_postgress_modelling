======= Sparkify database

Sparkify database contains information about Sparkifys' users, their activities and has been developed for providing analytics and explorations. 
The DB comprises five main tables:
- users (Dimension. Attributes: attributes: user_id, first_name, last_name, gender, level)
- artists (Dimension. Attributes: artist_id, name, location, latitude, longitude)
- songs (Dimension. Attributes: song_id, title, artist_id, year, duration)
- time (Dimension. Attributes: start_time, hour, day, week, month, year, weekday)
- songplays. (Fact. Attributes: songplays_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
These tables form star schema. For reasons of performance there aren't definite foreign key constraints.

======= Data 
Available data allow to provide such analysis for example as:
- most popular artist
- most active hours, weekdays and other periods
- users pereferences by location, gender
- paying categories by location or gender
and other

======= How to upload data
For uploading data into the DB it's needed to run next steps:
1. execute create_tables.py
2. execute etl_bulk_load.py
At the end of this file you can find all project files description

======= Tools for data analysis
Possibilities for data analytics and data scientists:
- test.ipynb - It's a Jupyter notebook with IPython extension. It's possible to run different ad-hoc queries 
- result.ipynb - It's possible to create different dasboards using Dataframes

======= Files description
- create_tables.py. Python script that created database with tables. Please keep in mind starting this file delete all objects first
- etl_bulk_load.py. Python script for uploading data into the database using bulk load
- etl.py. Python script for uploading data into the database row by row
- sql_queries.py. DDL scripts, SQL queries for selecting and inserting data


======= Notes for a mentor
There are two scripts for uploading data into the DB
- etl.py. This script provide loading data row by row approach
- etl_bulk_load.py. For the biggest table (songplays) I used bulk loading approach. Firstly data from all the log_data files are combined in one CSV file. And then all data are loaded into the main table (songplays) using stage layer

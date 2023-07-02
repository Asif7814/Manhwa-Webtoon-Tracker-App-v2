# This will be version 2 of the webtoon/manhwa tracker
# New inclusions: use of classes, MySQL as a database (a db where I manually input info), simple GUI (doesn't have to look amazing rn)

# series description includes: title, author, genres, user's status, current chapter, latest chapter, 
# publishing status, release day info (release days [ex. Sundays], next release date [ex. Sunday, May 14, 2023])

import mysql.connector

manhwa_webtoon_db = mysql.connector.connect(
    host ="localhost",
    user="root",
    passwd="(-c6w4d4b5i2f3-)",
    database="manhwa_webtoon_db"
)

mycursor = manhwa_webtoon_db.cursor()

def read_tb():
    where = 'user_status'
    where_specific = 'Reading'
    order_by = 'title'

    sql = f"SELECT title, current_chapter, latest_chapter FROM webtoon_tracker_tb WHERE {where} = '{where_specific}' ORDER BY {order_by}"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    for row in myresult:
        print(row) 

def add_new_series(series_descriptions):
    sql = "INSERT INTO webtoon_tracker_tb (title, author, genres, user_status, current_chapter, latest_chapter, publishing_status, release_day, upcoming_release, poster_image_dir) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.executemany(sql, series_descriptions)
    manhwa_webtoon_db.commit()

def update_series():
    #test
    set_input = 'poster_image_dir'
    user_input_1 = 'C:/Users/ashad/Documents/python_programs/practical_projects/manhwa_webtoon_tracker_v2_posters/Omniscient_Reader_Poster.png'

    where_input = 'title'
    user_input_2 = 'Omniscient Reader'

    sql = f"UPDATE webtoon_tracker_tb SET {set_input} = '{user_input_1}' WHERE {where_input} = '{user_input_2}'"
    mycursor.execute(sql)
    manhwa_webtoon_db.commit()

def delete_series():
    title = "Lookism"

    sql = f"DELETE FROM webtoon_tracker_tb WHERE title = '{title}'"

    mycursor.execute(sql)

    manhwa_webtoon_db.commit()

# This is version 2 of my manwha-webtoon-tracker-app

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

import mysql.connector

manhwa_webtoon_db = mysql.connector.connect(
    host ="localhost",
    user="root",
    passwd="(-c6w4d4b5i2f3-)",
    database="manhwa_webtoon_db"
)

mycursor = manhwa_webtoon_db.cursor()

series_description = ["","","","","","","","","",""]

def add_another_series():
    if messagebox.askyesno(title="Add Another Series Choice", message="Would you like to add another series?"):
        add_new_series()
    else:
        pass

def add_new_series():
    add_window = Toplevel()

    add_window.title("Add New Series")
    add_window.geometry("550x300")
    add_window.config(background="#001e00")

    bw_title_label = Label(add_window, text="Add New Series", font=("Arial", 12, 'bold'), fg="white", bg="#001e00")
    bw_title_label.place(x=180,y=10)

    def create_series_form():
        def submit():
            series_description[0] = x_title.get()
            series_description[1] = author.get()
            series_description[2] = genres.get()
            series_description[3] = user_status.get()
            series_description[4] = current_ch.get()
            series_description[5] = latest_ch.get()
            series_description[6] = publishing_status.get()
            series_description[7] = weekly_release_day.get()
            series_description[9] = image_file_path

            sql = "INSERT INTO webtoon_tracker_tb (title, author, genres, user_status, current_chapter, latest_chapter, publishing_status, release_day, upcoming_release, poster_image_dir) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            mycursor.execute(sql, series_description)
            manhwa_webtoon_db.commit()

            add_window.destroy()

            add_another_series()

        def search_image():
            global image_file_path
            image_file_path = filedialog.askopenfilename(initialdir="C:\\Users\\ashad\\Documents\\python_programs\\practical_projects\\manhwa_webtoon_tracker_v2_posters",
                                                         title="Search Poster Image",
                                                         filetypes=(("jpg files","*.jpg"), ("png files","*.png")))
            

        add_image_button = Button(add_window, text="+", font=("Arial", 12, 'bold'), fg="white", bg="#001e00", 
                        activeforeground="white", activebackground="#001e00", width=13, height=10, command=search_image)
        
        add_image_button.place(x=20,y=45)
        
        series_form = Frame(add_window)

        x_label = 0
        x_entry = 125

        label_width = 15
        entry_width = 30
        
        def enable_disable_wrd(e):
            if publishing_status.get() == "Ongoing" or user_status.get() == "Reading" or user_status.get() == "On Hold":
                weekly_release_day.config(value=["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
                weekly_release_day.current(0)
                
            if  publishing_status.get() == "Complete" or user_status.get() == "Finished":
                weekly_release_day.config(value =[" "])
                weekly_release_day.current(0)

        def add_series_entry(series_name, y_val):        
            add_entry_label = Label(series_form, text=series_name, font=("Arial", 10, 'bold'), fg="white", bg="#001e00", width=label_width).place(x=x_label,y=y_val)
            add_entry = Entry(series_form, font=("Arial", 10, 'bold'), fg="white", bg="#001e00", width=entry_width,
                            highlightbackground="green", highlightthickness=1)

            add_entry.place(x=x_entry,y=y_val)

            return add_entry

        def add_series_drop_down(series_name, series_list, y_val):
            add_drop_down_label = Label(series_form, text=series_name, font=("Arial", 10, 'bold'), fg="white", bg="#001e00", width=label_width).place(x=x_label,y=y_val)
            add_drop_down = ttk.Combobox(series_form, value=series_list)
           
            add_drop_down.current(0)
            add_drop_down.place(x=x_entry,y=y_val)

            return add_drop_down

        x_title = add_series_entry("Title", 0)

        author = add_series_entry("Author", 25)

        genres_list = ["Action", "Comedy", "Drama", "Fantasy", "Mystery", "Romance", "Sports", "Supernatural"]
        genres = add_series_drop_down("Genres", genres_list, 50)

        user_statuses_list = ["Reading", "Finished", "On Hold", "Plan To Read"]
        user_status = add_series_drop_down("Status", user_statuses_list, 75)
        user_status.bind("<<ComboboxSelected>>", enable_disable_wrd)

        publishing_statuses_list = ["Ongoing", "Complete", "On Hiatus"]
        publishing_status = add_series_drop_down("Publishing Status", publishing_statuses_list, 100)
        publishing_status.bind("<<ComboboxSelected>>", enable_disable_wrd)

        current_ch = add_series_entry("Current Ch", 125)

        latest_ch = add_series_entry("Latest Ch", 150)

        weekdays_list = [" "]
        weekly_release_day = add_series_drop_down("Release Days", weekdays_list, 175)

        series_form.config(background="white", width=350,height=200)
        series_form.place(x=180, y=45)

        submit_button = Button(add_window, text="Submit", font=("Arial", 10, 'bold'), fg="white", bg="#001e00", command=submit)
        submit_button.place(x=285, y=260)

    create_series_form()

def get_series_descs(u_status):
    series_descriptions = []

    sql = "SELECT * FROM webtoon_tracker_tb WHERE user_status = %s ORDER BY title"
    mycursor.execute(sql, u_status)

    myresult = mycursor.fetchall()

    for row in myresult:
        series_descriptions.append(row)

    return series_descriptions

def click_series(series_desc):    
    series_desc_window = Toplevel()
    series_desc_window.title("Series Description (temp)")
    series_desc_window.geometry("600x500")
    series_desc_window.config(background="#001e00")
    
    image_label = Label(series_desc_window, width=200, height=285, bg="black", image=default_img)
    image_label.place(x=30,y=60)

    def create_desc_placeholder(desc_name, desc, x, y):
        label = Label(series_desc_window, text=desc_name, font=("Arial", 11, "bold"), fg="white", bg="#181818").place(x=x,y=y)
        placeholder = Label(series_desc_window, text=desc, font=("Arial", 11, "bold"), fg="white", bg="#181818").place(x=x,y=y+25)
    
    author = create_desc_placeholder("AUTHOR", series_desc[1], 265, 60)
    genre = create_desc_placeholder("GENRES", series_desc[2], 265, 120)
    publishing_status = create_desc_placeholder("STATUS", series_desc[6], 425, 60)
    weekly_release = create_desc_placeholder("WEEKLY RELEASE", series_desc[7], 425, 120)
    
    title_placeholder = Label(series_desc_window, text=series_desc[0], font=("Arial", 12, "bold"), fg="white", bg="#181818").place(x=30,y=355)
    
    grey_box1 = Label(series_desc_window, bg="#6e6e6e", width=30,height=2).place(x=70, y=413)
    user_status = Label(series_desc_window, text=series_desc[3], font=("Arial", 12, "bold"), fg="white", bg="#6e6e6e").place(x=140,y=420)
    
    grey_box2 = Label(series_desc_window, bg="#6e6e6e", width=30,height=2).place(x=315, y=413)
    chapters = Label(series_desc_window, text=f"{series_desc[4]} / {series_desc[5]} CH", font=("Arial", 12, "bold"), fg="white", bg="#6e6e6e").place(x=370,y=420)

    green_stripe = Label(series_desc_window, bg="green", width=600, height=1).place(x=0,y=10)
    upcoming_release_in = Label(series_desc_window, text=f"Chapter {series_desc[5]+1} in {upcoming_release}", font=("Arial", 8, "bold"), fg="white", bg="green").place(x=240,y=10)

class Series:
    def __init__(self, series_desc, coords, collective_series_frame) -> None:
        self.series_desc = series_desc
        self.coords = coords
        self.collective_series_frame = collective_series_frame

    def display_series(self):
        series_container_button = Button(self.collective_series_frame, command = lambda: click_series(self.series_desc), text=(f"{self.series_desc[0]}\nCh {self.series_desc[4]} / {self.series_desc[5]}\nCh {self.series_desc[5]+1} in {upcoming_release}"),
                                        font=("Arial", 8, 'bold'), fg="white", bg="#181818", activeforeground="white", activebackground="#181818",
                                        highlightbackground="green", highlightthickness=3, image=default_img, compound="top", width=200, height=285)
        
        series_container_button.grid(row=self.coords[0], column=[self.coords[1]], padx=5, pady=5)

def display_collective_series(series_descs, y_coord):
    collective_series_frame = Frame(main_window)
    collective_series_frame.config(background="#001e00")
    
    r = 0
    c = 0

    count = 0

    for i in range(len(series_descs)):
        series = Series(series_descs[i], [r,c], collective_series_frame)

        series.display_series()

        c+=1
        count += 1

        if count == 4:
            r+=1
            c=0

    collective_series_frame.place(x=200, y=y_coord)

main_window = Tk()

main_window.title("Series Tracker")
main_window.geometry("1400x800")
main_window.config(background="#001e00")

default_img = PhotoImage(file="C:\\Users\\ashad\\Documents\\python_programs\\practical_projects\\webtoon_logo.png")

title_label = Label(main_window, text="Webtoon", font=("Arial", 14, 'bold'), fg="white", bg="#001e00",
                    highlightbackground="green", highlightthickness=2)
title_label.place(x=635,y=40)

search_bar_entrybox = Entry(main_window, font=("Arial", 12, 'bold'), fg="white", bg="#001e00",
                            highlightbackground="white", width=23)

search_bar_entrybox.insert(0, "Search")

search_bar_entrybox.place(x=950,y=45)

add_new_series_button = Button(main_window, text="+", command=add_new_series, width=3, height=1,
                               font=("Arial", 14, 'bold'), fg="white", bg="#001e00").place(x=1200, y=40)

#THESE ARE TEMP VALUES
upcoming_release="X days (Incomplete)" # haven't started implementing time feature yet
temp_image = PhotoImage(file='C:\\Users\\ashad\\Documents\\python_programs\\practical_projects\\manhwa_webtoon_tracker_v2_posters\\Lookism_Poster.png') #attempting to work out how to add poster to specified series

series_descs_r = get_series_descs(("Reading", ))
series_descs_p = get_series_descs(("Plan To Read", ))

y_coord = 100

display_collective_series(series_descs_r, y_coord)

main_window.mainloop()
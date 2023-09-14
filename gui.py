import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import cursor
import functions
from datetime import datetime

try:
    cnx = mysql.connector.connect(user='Josh', password='TempPassword', host='127.0.0.1', database='sunlab')
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
def mainMenu():
    app = tk.Tk()
    app.title("Main Menu")
    entry = tk.Entry(app)

    def create_label(text):
        label = tk.Label(app, text=text)
        label.pack()

    def text_box():
        entry.pack()

    def read_textbox():
        return entry.get()

    def login_button():
        button = tk.Button(app, text="Login as Admin", command=login_click)
        button.pack()

    def login_click():
        result = functions.searchTableId(read_textbox())
        if result:
            id, name, type, status = result
            if type == "Admin":
                adminMenu()
            else:
                create_label("Not an Admin")
        else:
            create_label("Could not find Admin")

    def swipe_button_in():
        button = tk.Button(app, text="Swipe In", command=swipe_click_in)
        button.pack()

    def swipe_click_in():
        if functions.swipe(read_textbox()) == 1:
            create_label("Success")
            result = functions.searchTableId(read_textbox());

            id, name, type, status = result

            data = {
                "id": id,
                "name": name,
                "Date": datetime.now(),
                "InOrOut": "In"
            }

            insert_query = "INSERT INTO users (id, name, Date, InOrOut) VALUES (%(id)s, %(name)s, %(Date)s, %(InOrOut)s)"

            try:
                cursor.execute(insert_query, data)
                cnx.commit()
                print("Data inserted successfully!")

            except mysql.connector.Error as err:
                cnx.rollback()
                print(f"Error inserting data: {err}")
        if functions.search_status(read_textbox()) == 1:
            functions.insert_timestamp(read_textbox())
        elif functions.swipe(read_textbox()) == 0:
            create_label("Denied. Please contact an Admin")
        else:
            create_label("Please insert a correct ID")

    def swipe_button_out():
        button = tk.Button(app, text="Swipe Out", command=swipe_click_out)
        button.pack()

    def swipe_click_out():
        if functions.swipe(read_textbox()) == 1:
            create_label("Success")
            result = functions.searchTableId(read_textbox());

            id, name, type, status = result

            data = {
                "id": id,
                "name": name,
                "Date": datetime.now(),
                "InOrOut": "Out"
            }

            insert_query = "INSERT INTO users (id, name, Date, InOrOut) VALUES (%(id)s, %(name)s, %(Date)s, %(InOrOut)s)"

            try:
                cursor.execute(insert_query, data)
                cnx.commit()
                print("Data inserted successfully!")

            except mysql.connector.Error as err:
                cnx.rollback()
                print(f"Error inserting data: {err}")

        if functions.search_status(read_textbox()) == 1:
            functions.insert_timestamp(read_textbox())
        elif functions.swipe(read_textbox()) == 0:
            create_label("Denied. Please contact an Admin")
        else:
            create_label("Please insert a correct ID")

    create_label("Insert ID here:")
    text_box()
    swipe_button_in()
    swipe_button_out()
    login_button()
    app.mainloop()
def adminMenu():
    app = tk.Tk()
    app.title("Admin Menu")

    def create_label(text):
        label = tk.Label(app, text=text)
        label.pack()

    def view_history_button():
        button = tk.Button(app, text="View History", command=view_history_click)
        button.pack()

    def view_history_click():
        view_history_menu()

    def edit_student_access_button():
        button = tk.Button(app, text="Edit Student Access", command=edit_student_access_click)
        button.pack()

    def edit_student_access_click():
        edit_student_access_menu()

    create_label("Please select one")
    view_history_button()
    edit_student_access_button()
    app.mainloop()

def view_history_menu():
    app = tk.Tk()
    app.title("View History Menu")
    entry = tk.Entry(app)
    functions.delete_5_years()

    def create_label(text):
        label = tk.Label(app, text=text)
        label.pack()

    def text_box():
        entry.pack()

    def read_textbox():
        return entry.get()

    def displayTimestampTable(filter):

        timestamp_table = ttk.Treeview(app, columns=("ID", "Name", "Time Stamp", "In/Out"))
        timestamp_table.heading("#1", text="ID")
        timestamp_table.heading("#2", text="Name")
        timestamp_table.heading("#3", text="Date")
        timestamp_table.heading("#4", text="In/Out")

        timestamp_table.pack()

        cursor.execute("SELECT * FROM users")

        for row in cursor.fetchall():
            timestamp_table.insert("", "end", values=row)

        if filter == "reset":
            timestamp_table = ttk.Treeview(app, columns=("ID", "Name", "Time Stamp", "In/Out"))
            timestamp_table.heading("#1", text="ID")
            timestamp_table.heading("#2", text="Name")
            timestamp_table.heading("#3", text="Date")
            timestamp_table.heading("#4", text="In/Out")

            timestamp_table.pack()

            cursor.execute("SELECT * FROM users")

            for row in cursor.fetchall():
                timestamp_table.insert("", "end", values=row)

        if filter == "id":
            existing_data = timestamp_table.get_children()
            updated_data = functions.searchTableIdAdmin(read_textbox())

            for item in existing_data:
                timestamp_table.delete(item)

            timestamp_table.pack_forget()

            timestamp_table = ttk.Treeview(app, columns=("ID", "Name", "Time Stamp", "In/Out"))
            timestamp_table.heading("#1", text="ID")
            timestamp_table.heading("#2", text="Name")
            timestamp_table.heading("#3", text="Date")
            timestamp_table.heading("#4", text="In/Out")

            timestamp_table.pack()

            for row in updated_data:
                timestamp_table.insert("", "end", values=row)

        if filter == "name":
            existing_data = timestamp_table.get_children()
            updated_data = functions.searchTableNameAdmin(read_textbox())

            for item in existing_data:
                timestamp_table.delete(item)

            timestamp_table.pack_forget()

            timestamp_table = ttk.Treeview(app, columns=("ID", "Name", "Time Stamp", "In/Out"))
            timestamp_table.heading("#1", text="ID")
            timestamp_table.heading("#2", text="Name")
            timestamp_table.heading("#3", text="Date")
            timestamp_table.heading("#4", text="In/Out")

            timestamp_table.pack()

            for row in updated_data:
                timestamp_table.insert("", "end", values=row)

        if filter == "date":
            existing_data = timestamp_table.get_children()
            updated_data = functions.searchTableDateAdmin(read_textbox())

            for item in existing_data:
                timestamp_table.delete(item)

            timestamp_table.pack_forget()

            timestamp_table = ttk.Treeview(app, columns=("ID", "Name", "Time Stamp", "In/Out"))
            timestamp_table.heading("#1", text="ID")
            timestamp_table.heading("#2", text="Name")
            timestamp_table.heading("#3", text="Date")
            timestamp_table.heading("#4", text="In/Out")

            timestamp_table.pack()

            for row in updated_data:
                timestamp_table.insert("", "end", values=row)

        if filter == "range":
            existing_data = timestamp_table.get_children()
            updated_data = functions.searchTableRangeAdmin(read_textbox())

            for item in existing_data:
                timestamp_table.delete(item)

            timestamp_table.pack_forget()

            timestamp_table = ttk.Treeview(app, columns=("ID", "Name", "Time Stamp", "In/Out"))
            timestamp_table.heading("#1", text="ID")
            timestamp_table.heading("#2", text="Name")
            timestamp_table.heading("#3", text="Date")
            timestamp_table.heading("#4", text="In/Out")

            timestamp_table.pack()

            for row in updated_data:
                timestamp_table.insert("", "end", values=row)


    def search_date_button():
        button = tk.Button(app, text="Search Date", command=search_date_click)
        button.pack()

    def search_date_click():
        displayTimestampTable("date")

    def search_id_button():
        button = tk.Button(app, text="Search ID", command=search_id_click)
        button.pack()

    def search_id_click():
        displayTimestampTable("id")

    def search_name_button():
        button = tk.Button(app, text="Search Name", command=search_name_click)
        button.pack()

    def search_name_click():
        displayTimestampTable("name")

    def search_range_button():
        button = tk.Button(app, text="Search Time Range", command=search_range_click)
        button.pack()

    def search_range_click():
        displayTimestampTable("range")

    def reset_button():
        button = tk.Button(app, text="Reset Table", command=reset_click)
        button.pack()

    def reset_click():
        displayTimestampTable("reset")

    displayTimestampTable("none")
    reset_button()
    text_box()
    search_id_button()
    text_box()
    search_name_button()
    text_box()
    create_label("Please use format 'MM/DD/YYYY' for date and 'MM/DD/YYYY-MM/DD/YYYY' for time range.")
    search_date_button()
    text_box()
    text_box()
    search_range_button()
    app.mainloop()

def edit_student_access_menu():
    app = tk.Tk()
    app.title("Edit Student Access Menu")
    entry = tk.Entry(app)

    def create_label(text):
        label = tk.Label(app, text=text)
        label.pack()

    def text_box():
        entry.pack()

    def read_textbox():
        return entry.get()

    def activate_button():
        button = tk.Button(app, text="Activate", command=activate_click)
        button.pack()

    def activate_click():
        functions.activate(read_textbox(), app)

    def deactivate_button():
        button = tk.Button(app, text="Deactivate", command=deactivate_click)
        button.pack()

    def deactivate_click():
        functions.deactivate(read_textbox(), app)

    create_label("Insert student's ID you wish to change")
    text_box()
    activate_button()
    deactivate_button()
    app.mainloop()




import mysql.connector
from mysql.connector import cursor
import tkinter as tk
from datetime import datetime, timedelta

try:
    cnx = mysql.connector.connect(user='Josh', password='TempPassword', host='127.0.0.1', database='sunlab')
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
def searchTableId(id):
    search_crit = id
    search_query = "SELECT * FROM status where id = %s"

    try:
        cursor.execute(search_query, (search_crit,))
        result = cursor.fetchone()
        return result

    except mysql.connector.Error as err:
        print(f"Error searching for id: {err}")

def searchTableName(name):
    search_crit = name
    search_query = "SELECT * FROM status where name = %s"

    try:
        cursor.execute(search_query, (search_crit,))
        result = cursor.fetchone()
        return result

    except mysql.connector.Error as err:
        print(f"Error searching for person: {err}")

def activate(id, app):

    result = searchTableId(id)

    if result:
        id, name, type, status = result
        if status == "Active":
            label = tk.Label(app, text="already activated")
            label.pack()
            return
        elif status == "Inactive":
            update_query = "UPDATE status SET status = %s Where id = %s"
            try:
                cursor.execute(update_query, ("Active", id))
                cnx.commit()
                label = tk.Label(app, text="activated")
                label.pack()
            except mysql.connector.Error as err:
                print(f"Error updating status: {err}")


def deactivate(id, app):

    result = searchTableId(id)

    if result:
        id, name, type, status = result
        if status == "Inactive":
            label = tk.Label(app, text="already deactivated")
            label.pack()
            return
        elif status == "Active":
            update_query = "UPDATE status SET status = %s Where id = %s"
            try:
                cursor.execute(update_query, ("Inactive", id))
                cnx.commit()
                label = tk.Label(app, text="deactivated")
                label.pack()
            except mysql.connector.Error as err:
                print(f"Error updating status: {err}")

def swipe(id):
    result = searchTableId(id)
    if result:
        id, name, type, status = result
        if status == "Active":
            return 1
        else:
            return 0

def search_status(id):

    result = searchTableId(id)

    if result:
        id, name, type, status = result
        if status == "Active":
            return 1
        else:
            return 0

def insert_timestamp(id):

    result = searchTableId(id)

    if result:
        id, name, type, status = result

def searchTableNameAdmin(name):
    search_crit = name
    search_query = "SELECT * FROM users where name = %s"

    try:
        cursor.execute(search_query, (search_crit,))
        result = cursor.fetchall()
        return result

    except mysql.connector.Error as err:
        print(f"Error searching for name: {err}")

def searchTableDateAdmin(date):
    search = datetime.strptime(date,"%m/%d/%Y")
    search_query = "SELECT * FROM users where Date = %s"

    try:
        cursor.execute(search_query, (search,))
        result = cursor.fetchall()
        return result

    except mysql.connector.Error as err:
        print(f"Error searching for Date: {err}")

def searchTableIdAdmin(id):
    search_crit = id
    search_query = "SELECT * FROM users where id = %s"

    try:
        cursor.execute(search_query, (search_crit,))
        result = cursor.fetchall()
        return result

    except mysql.connector.Error as err:
        print(f"Error searching for id: {err}")

def searchTableRangeAdmin(date):
    start_date_str, end_date_str = date.split('-')
    start_date_object = datetime.strptime(start_date_str, "%m/%d/%Y")
    end_date_object = datetime.strptime(end_date_str, "%m/%d/%Y")

    search_query = "SELECT * FROM users where Date BETWEEN %s AND %s"

    try:
        cursor.execute(search_query, (start_date_object, end_date_object))
        result = cursor.fetchall()
        return result

    except mysql.connector.Error as err:
        print(f"Error searching for Date: {err}")

def delete_5_years():
    search_crit = datetime.now() - timedelta(days=5*365)
    delete_query = "DELETE FROM users WHERE Date <= %s"
    cursor.execute(delete_query, (search_crit,))


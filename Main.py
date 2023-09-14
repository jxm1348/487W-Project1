import mysql.connector
import gui


try:
    cnx = mysql.connector.connect(user='Josh', password='TempPassword', host='127.0.0.1', database='sunlab')
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")

gui.mainMenu()

cnx.close()
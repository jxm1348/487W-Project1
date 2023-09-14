import mysql.connector
from mysql.connector import cursor

try:
    cnx = mysql.connector.connect(user='Josh', password='TempPassword', host='127.0.0.1', database='sunlab')
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")


statusData = [
    (123456789, "Alice Johnson", "Student", "Active"),
    (987654321, "Bob Smith", "Student", "Active"),
    (246813579, "Charlie Brown", "Student", "Active"),
    (135792468, "David Williams", "Student", "Active"),
    (654321987, "Emma Davis", "Staff", "Active"),
    (369258147, "Frank Wilson", "Staff", "Active"),
    (753159864, "Grace Lee", "Student", "Active"),
    (582746913, "Helen Turner", "Admin", "Active"),
    (896547132, "Ian Miller", "Staff", "Active"),
]


insert_query = "INSERT INTO status (id, name, type, status) VALUES (%s, %s, %s, %s)"

try:
    cursor.executemany(insert_query, statusData)
    cnx.commit()
    print("Data inserted successfully!")

except mysql.connector.Error as err:
    cnx.rollback()
    print(f"Error inserting data: {err}")

cnx.close()
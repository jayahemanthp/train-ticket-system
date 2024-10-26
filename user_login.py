#Use MySQL db to store user details
#Use db to store train details
#retrieve data, modify data, display data


import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin@123"
)
mycursor = mydb.cursor()
try:
    mycursor.execute("CREATE DATABASE ticket_system")
except:
    pass
mycursor.execute("USE ticket_system")

mycursor.execute("SHOW TABLES LIKE 'users'")
result = mycursor.fetchone()
if not result:
    mycursor.execute("""
        CREATE TABLE users (
            username VARCHAR(255),
            password VARCHAR(255) NOT NULL,
            PRIMARY KEY (username)
        )
    """)
    mydb.commit()
    print("Table 'users' created successfully.")

import dashboard

def user_login(username, password):
    try:
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        val = (username, password)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        if myresult:
            print("Login successful!")
            return True
        else:
            print("Login failed. Invalid username or password.")
            return False
    except mysql.connector.Error as error:
        print("MySQL Error:", error)
        return False

def register_user(username, password):
    try:
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, password)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Registration successful!")
    except mysql.connector.Error as error:
        print("MySQL Error:", error)

def main():
    while True:
        print()
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        print()
        choice = input("Enter your choice: ")
        print()

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if user_login(username, password):
                dashboard.options(username)
                break
        elif choice == "2":
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            register_user(username, password)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again")

main()
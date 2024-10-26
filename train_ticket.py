#Use MySQL db to store user details
#Use db to store train details
#retrieve data, modify data, display data

#Damn gonna be harder than expected

import mysql.connector
import csv

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="your_database"
)
mycursor = mydb.cursor()
mycursor.execute("SHOW TABLES LIKE 'users'")
result = mycursor.fetchone()
if result:
    print("Table 'users' already exists.")
else:
    mycursor.execute("""
        CREATE TABLE users (
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
        )
    """)
    mydb.commit()
    print("Table 'users' created successfully.")

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
        print("Error connecting to MySQL database:", error)
        return False
    finally:
        if mydb:
            mycursor.close()
            mydb.close()

def register_user(username, password):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="your_database"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, password)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Registration successful!")
    except mysql.connector.Error as error:
        print("Error connecting to MySQL database:", error)
    finally:
        if mydb:
            mycursor.close()
            mydb.close()

def save_to_csv(data):
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def main():
    while True:
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if user_login(username, password):
                data = [username, password]
                save_to_csv(data)
                print("Data saved to CSV file.")
        elif choice == "2":
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            register_user(username, password)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again")

if __name__ == "__main__":
    main()


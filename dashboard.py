# use add_trains to add trains, note: this is not a login function, to be added before user login
# display train: retrieve data from db and show train details, book tickets
# dummy payment function

import mysql.connector
import tickets

mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin@123",
    database="ticket_system"
)
mycursor = mydb.cursor()
mycursor.execute("SHOW TABLES LIKE 'trains'")
result = mycursor.fetchone()
if not result:
    mycursor.execute("""
        CREATE TABLE trains (
            train_no CHAR(6) PRIMARY KEY,
            train_name VARCHAR(255) NOT NULL,         
            from_loc VARCHAR(255) NOT NULL,
            to_loc VARCHAR(255) NOT NULL,
            seats INT NOT NULL,        
            cost INT NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL
        )
    """)
    mydb.commit()
    print("Table 'trains' created successfully.")

def add_trains(): #not connected to user login, to be run separately
    while True:
        print()
        train_no = input("Enter Train Number (6 digit): ")
        name = input("Enter Train Name: ")
        from_loc = input("Enter From City: ")
        to_loc = input("Enter To City: ")
        seats = input("Enter Total Seats: ")
        cost = input("Enter cost of a ticket: ")
        start = input("Enter start time (hh:mm): ")
        end = input("Enter end time (hh:mm): ")
        try:
            sql = "INSERT INTO trains (train_no, train_name, from_loc, to_loc, seats, cost, start_time, end_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (train_no, name, from_loc, to_loc, seats, cost, start, end)
            mycursor.execute(sql, val)
            mydb.commit()
            print("Added train successfully!")
        except mysql.connector.Error as error:
            print("Error connecting to MySQL database:", error)
        print()
        cont = input('Do you want to continue? (y/n)')
        if cont not in 'Yy':
            break
        
#add_trains()


def display_trains(user_id):
    locations = [
    "Mumbai",
    "Delhi",
    "Kolkata",
    "Chennai",
    "Bengaluru",
    "Hyderabad",
    "Ahmedabad",
    "Pune",
    "Jaipur",
    "Lucknow"]
    n = 1
    for city in locations:
        print(f'{n}. {city}')
        n+=1
    print()

    #get details
    from_loc = input("Enter From City from the list: \t")
    to_loc = input("Enter To City from the list: \t")
    if not (from_loc in locations and to_loc in locations):
        print("Invalid input! Try again")
        return

    date = input("Enter Date of travel: \t\t")
    psgr_no = int(input("Enter no. of passengers: \t"))

    #fetch details of trains based on this info from database
    try:
        sql = "SELECT train_no,train_name,seats,cost,start_time,end_time FROM trains WHERE from_loc = %s AND to_loc = %s"
        val = (from_loc, to_loc)
        mycursor.execute(sql, val)
        trains = mycursor.fetchall()
        if trains:
            print("Available trains:\n")
            for train in trains:
                print(train[1])
                print(f"Train Number: \t{train[0]}") # need to print in better format
                print(f"Ticket Cost: \tRs.{train[3]}")
                print(f"Departure: \t{train[4]}")
                print(f"Arrival: \t{train[5]}")
                seats = train[2] - tickets.booked(train[0],date)
                print(f"Seat Available: {seats}\n")
            tickets.booking(user_id, from_loc, to_loc, date, psgr_no)
        else:
            print("No trains found.")
    except mysql.connector.Error as error:
        print("MySQL Error:", error)


def options(user):
    while True:
        print()
        print("1. Book Ticket")
        print("2. View Booked Tickets")
        print("3. Exit")
        print()
        choice = input("Enter your choice: ")
        print()

        if choice == "1":
            display_trains(user)
        elif choice == "2":
            tickets.display_tickets(user)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again")    

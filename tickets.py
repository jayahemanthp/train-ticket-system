#store tickets, retrieve tickets, book ticket

import mysql.connector
import time

mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin@123",
    database="ticket_system"
)
mycursor = mydb.cursor()
mycursor.execute("SHOW TABLES LIKE 'tickets'")
result = mycursor.fetchone()
if not result:
    mycursor.execute("""
        CREATE TABLE tickets (
            id CHAR(4) PRIMARY KEY,
            user_id VARCHAR(255),         
            train VARCHAR(255) NOT NULL,   
            from_loc VARCHAR(255) NOT NULL,
            to_loc VARCHAR(255) NOT NULL,         
            passenger_name VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            berth_pref VARCHAR(10),
            date DATE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(username)
        )
    """)
    mydb.commit()
    print("Table 'tickets' created successfully.")

def make_payment(cost,psgr_no):
    total = cost*psgr_no

    while True:
        print(f"Total cost: Rs.{total}\n")
        print("Select Payment Method")
        print("1. Card")
        print("2. Net Banking")
        print("3. UPI")
        print("4. Cancel Payment")
        print()
        choice = input("Enter your choice: ")
        print()

        if choice == "1":
            card = input("Enter card number: ")
            month = input("Enter expiry month (mm/yy): ")
            cvv = input("Enter cvv number: ")
            if len(card) != 16 or int(month.split('/')[-1]) < 24 or len(cvv) != 3:
                print("Invalid card details! Try again.")
                continue
            print("Processing payment...\n")
            time.sleep(3)
            otp = input("Enter OTP number: ")
            if len(otp) != 6:
                print("Invalid OTP! Try again.")
                continue
            print("Verifying OTP...\n")
            time.sleep(3)
            return True
        elif choice == "2":
            user_name = input("Enter net banking username: ")
            password = input("Enter password: ")
            print("Processing payment...\n")
            time.sleep(3)
            otp = input("Enter OTP number: ")
            if len(otp) != 6:
                print("Invalid OTP! Try again.")
                continue
            print("Verifying OTP...\n")
            time.sleep(3)
            return True
        elif choice == "3":
            upi = input("Enter UPI id: ")
            if '@' not in upi:
                print("Invalid UPI id! Try again.")
                continue
            print("Processing payment...\n")
            time.sleep(3)
            pin = input("Enter UPI PIN: ")
            if len(pin) != 4:
                print("Invalid PIN! Try again.")
                continue
            print("Verifying PIN...\n")
            time.sleep(3)
            return True
        else:
            return False
        
def booked(train,date):
    mycursor.execute("SELECT * FROM tickets WHERE train = %s AND date = %s",(train,date))
    seats = len(mycursor.fetchall())
    return seats


def book_ticket(user_id,train,from_loc,to_loc,name,age,berth,date):
    try:
        mycursor.execute("SELECT * FROM tickets")
        id = len(mycursor.fetchall())+1
        sql = "INSERT INTO tickets (id, user_id, train, from_loc, to_loc, passenger_name, age, berth_pref, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (id,user_id,train,from_loc,to_loc,name,age,berth,date)
        mycursor.execute(sql, val)
        mydb.commit()
        print(f"Ticket booked for {name} successfully!")
    except mysql.connector.Error as error:
        print("MySQL Error:", error)

def booking(user_id, from_loc, to_loc, date, psgr_no):
    try:
        train = input("Enter train number: ")
        mycursor.execute("SELECT * FROM trains WHERE train_no = %s",(train,))
        fetched = mycursor.fetchone()
        if fetched:
            cost = fetched[5]
        else:
            print("Invalid train number!")
            return
        psgrs = []
        for i in range(psgr_no):
            print(f"Passenger {i+1} Details")
            name = input("Enter Passenger name: ")
            age = input("Enter age: ")
            berth = input("Enter berth preference: ")
            psgrs.append((name,age,berth))
            print()
        
        if make_payment(cost, psgr_no):
            print("Payment Sucessful!\n")
            for psgr in psgrs:
                name,age,berth = psgr
                book_ticket(user_id,train,from_loc,to_loc,name,age,berth,date)
    except mysql.connector.Error as error:
        print("MySQL Error:", error)

def display_tickets(user):
    mycursor.execute("SELECT * FROM tickets WHERE user_id = %s", (user,))
    tickets = mycursor.fetchall()  

    for ticket in tickets:
        mycursor.execute("SELECT train_name,start_time,end_time FROM trains WHERE train_no = %s", (ticket[2],))
        train = mycursor.fetchone()  

        print(f"Ticket id: \t{ticket[0]}")
        print(f"Train number: \t{ticket[2]}\t\tTrain name: \t{train[0]}")

        print(f"Boarding from: \t{ticket[3]}\t\tBoarding time: \t{train[1]}")
        print(f"Destination: \t{ticket[4]}\t\tArrival time: \t{train[2]}")
        print(f"Passenger name: {ticket[5]}")
        print(f"Passenger age: \t{ticket[6]}\t\tBerth preference: \t{ticket[7]}")
        print(f"Date of travel: {ticket[8]}\n")


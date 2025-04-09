import mysql.connector
from datetime import datetime


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="roshini",
    database="library_db"
)
cursor = db.cursor()



def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    quantity = int(input("Enter quantity: "))
    cursor.execute("INSERT INTO books (title, author, quantity) VALUES (%s, %s, %s)", (title, author, quantity))
    db.commit()
    print("Book added successfully.\n")

def register_member():
    name = input("Enter member name: ")
    email = input("Enter member email: ")
    cursor.execute("INSERT INTO members (name, email) VALUES (%s, %s)", (name, email))
    db.commit()
    print("Member registered successfully.\n")

def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    print("\n--- Book List ---")
    for book in books:
        print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Quantity: {book[3]}")
    print()

def view_members():
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    print("\n--- Member List ---")
    for member in members:
        print(f"ID: {member[0]}, Name: {member[1]}, Email: {member[2]}")
    print()

def issue_book():
    book_id = int(input("Enter book ID: "))
    member_id = int(input("Enter member ID: "))
    issue_date = datetime.now().date()
    cursor.execute("SELECT quantity FROM books WHERE book_id = %s", (book_id,))
    result = cursor.fetchone()
    if result and result[0] > 0:
        cursor.execute("INSERT INTO issue (book_id, member_id, issue_date, return_date) VALUES (%s, %s, %s, %s)",
                       (book_id, member_id, issue_date, None))
        cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id = %s", (book_id,))
        db.commit()
        print("Book issued successfully.\n")
    else:
        print("Book not available or invalid book ID.\n")

def return_book():
    issue_id = int(input("Enter issue ID: "))
    return_date = datetime.now().date()
    cursor.execute("SELECT book_id FROM issue WHERE issue_id = %s AND return_date IS NULL", (issue_id,))
    result = cursor.fetchone()
    if result:
        book_id = result[0]
        cursor.execute("UPDATE issue SET return_date = %s WHERE issue_id = %s", (return_date, issue_id))
        cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE book_id = %s", (book_id,))
        db.commit()
        print("Book returned successfully.\n")
    else:
        print("Invalid issue ID or book already returned.\n")

def main_menu():
    while True:
        print("==== Library Management System ====")
        print("1. Add Book")
        print("2. Register Member")
        print("3. View Books")
        print("4. View Members")
        print("5. Issue Book")
        print("6. Return Book")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            add_book()
        elif choice == '2':
            register_member()
        elif choice == '3':
            view_books()
        elif choice == '4':
            view_members()
        elif choice == '5':
            issue_book()
        elif choice == '6':
            return_book()
        elif choice == '7':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

# Start the program
main_menu()

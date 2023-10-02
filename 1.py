import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="mxq111525",
    database="library_db"
)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        BookID VARCHAR(255) PRIMARY KEY,
        Title VARCHAR(255),
        Author VARCHAR(255),
        ISBN VARCHAR(255),
        Status VARCHAR(255)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID VARCHAR(255) PRIMARY KEY,
        Name VARCHAR(255),
        Email VARCHAR(255)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservations (
        ReservationID VARCHAR(255) PRIMARY KEY,
        BookID VARCHAR(255),
        UserID VARCHAR(255),
        ReservationDate VARCHAR(255),
        FOREIGN KEY (BookID) REFERENCES Books (BookID),
        FOREIGN KEY (UserID) REFERENCES Users (UserID)
    )
''')


def add_book():
    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = "Available"

    cursor.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (%s, %s, %s, %s, %s)",
                   (book_id, title, author, isbn, status))
    conn.commit()
    print("Book added successfully!")


def find_book_detail():
    book_id = input("Enter BookID: ")

    cursor.execute('''
        SELECT Books.Title, Books.Author, Books.ISBN, Books.Status, Users.Name, Users.Email
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
        WHERE Books.BookID = %s
    ''', (book_id,))

    result = cursor.fetchone()
    if result:
        book_title, author, isbn, status, user_name, user_email = result
        if user_name and user_email:
            print(f"Book Title: {book_title}")
            print(f"Author: {author}")
            print(f"ISBN: {isbn}")
            print(f"Status: {status}")
            print(f"Reserved by: {user_name} ({user_email})")
        else:
            print(f"Book Title: {book_title}")
            print(f"Author: {author}")
            print(f"ISBN: {isbn}")
            print(f"Status: {status}")
            print("Not reserved by any user.")
    else:
        print("Book not found!")


def find_reservation_status():
    text = input("Enter BookID, Title, UserID, or ReservationID: ")

    if text.startswith("LB"):
        cursor.execute('''
            SELECT Books.Title, Reservations.ReservationDate, Users.Name, Users.Email
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Books.BookID = %s
        ''', (text,))
    elif text.startswith("LU"):
        cursor.execute('''
            SELECT Books.Title, Reservations.ReservationDate
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            WHERE Reservations.UserID = %s
        ''', (text,))
    elif text.startswith("LR"):
        cursor.execute('''
            SELECT Books.Title, Reservations.ReservationDate, Users.Name, Users.Email
            FROM Reservations
            LEFT JOIN Books ON Reservations.BookID = Books.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Reservations.ReservationID = %s
        ''', (text,))
    else:
        cursor.execute('''
            SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, 
            Reservations.ReservationID, Users.Name, Users.Email, Reservations.ReservationDate
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Books.Title LIKE %s;
        ''', (f"%{text}%",))

    result = cursor.fetchall()
    if result:
        for row in result:
            if row[5]:
                print(f"BookID: {row[0]}")
                print(f"Title: {row[1]}")
                print(f"Author: {row[2]}")
                print(f"ISBN: {row[3]}")
                print(f"Status: {row[4]}")
                print(f"ReservationID: {row[5]}")
                print(f"Reserved by: {row[6]} ({row[7]})")
                print(f"Reservation Date: {row[8]}")
                print()
            else:
                print(f"BookID: {row[0]}")
                print(f"Title: {row[1]}")
                print(f"Author: {row[2]}")
                print(f"ISBN: {row[3]}")
                print(f"Status: {row[4]}")
                print("Not reserved by any user.")
                print()
    else:
        print("No matching records found!")


def find_all_books():
    cursor.execute('''
        SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, 
        Reservations.ReservationID, Users.Name, Users.Email, Reservations.ReservationDate
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID;
    ''')

    result = cursor.fetchall()
    if result:
        for row in result:
            if row[5]:
                print(f"BookID: {row[0]}")
                print(f"Title: {row[1]}")
                print(f"Author: {row[2]}")
                print(f"ISBN: {row[3]}")
                print(f"Status: {row[4]}")
                print(f"ReservationID: {row[5]}")
                print(f"Reserved by: {row[6]} ({row[7]})")
                print(f"Reservation Date: {row[8]}")
                print()
            else:
                print(f"BookID: {row[0]}")
                print(f"Title: {row[1]}")
                print(f"Author: {row[2]}")
                print(f"ISBN: {row[3]}")
                print(f"Status: {row[4]}")
                print("Not reserved by any user.")
                print()
    else:
        print("No books found in the database!")


def update_book_details():
    book_id = input("Enter BookID to update: ")
    new_status = input("Enter new status: ")

    cursor.execute("UPDATE Books SET Status = %s WHERE BookID = %s", (new_status, book_id))

    cursor.execute("DELETE FROM Reservations WHERE BookID = %s", (book_id,))

    conn.commit()
    print("Book details updated!")


def delete_book():
    book_id = input("Enter BookID to delete: ")

    cursor.execute("DELETE FROM Books WHERE BookID = %s", (book_id,))

    cursor.execute("DELETE FROM Reservations WHERE BookID = %s", (book_id,))

    conn.commit()
    print("Book deleted!")


# Main menu loop
while True:
    print("\nLibrary Management System")
    print("1. Add a new book to the database")
    print("2. Find a book's detail based on BookID")
    print("3. Find a book's reservation status based on BookID, Title, UserID, or ReservationID")
    print("4. Find all the books in the database")
    print("5. Modify/update book details based on its BookID")
    print("6. Delete a book based on its BookID")
    print("7. Exit")

    choice = input("Enter your choice (1/2/3/4/5/6/7): ")

    if choice == "1":
        add_book()
    elif choice == "2":
        find_book_detail()
    elif choice == "3":
        find_reservation_status()
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        update_book_details()
    elif choice == "6":
        delete_book()
    elif choice == "7":
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a valid option (1/2/3/4/5/6/7).")

# Close the database connection when done
conn.close()


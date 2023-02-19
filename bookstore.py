'''
Bookstore inventory using SQLite database
Users are able to add, update, delete and search books in the database.
'''

import sqlite3
from pprint import pprint       # Import pretty print

# Initialised variables
logged_in = True
book_id = 3007     # Book id to increment after data initialisation
books = [
    [3001, 'A Tale of Two Cities', 'Charles Dickens', 30],
    [3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K.Rowling', 40],
    [3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25],
    [3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37],
    [3005, 'Alice in Wonderland', 'Lewis Carroll', 12],
    [3006, 'Harry Potter and the Prisoner of Azkaban', 'J.K.Rowling', 30],
    [3007, 'Harry Potter and the Half Blood Prince', 'J.K.Rowling', 25]]

try:
    # Create file
    db = sqlite3.connect('ebookstore')
    cursor = db.cursor()        # Get a cursor object

    # Create table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books(
                id integer PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER, UNIQUE(Title, Author));
        ''')

    # Write books data into table
    cursor.executemany('''
        INSERT INTO books ('id', 'Title', 'Author', 'Qty') VALUES (?, ?, ?, ?)''', (books))
    print(f"All {cursor.rowcount} records have been entered.")

except sqlite3.OperationalError as e:
    # Roll back any change if something goes wrong
    db.rollback()
    raise e


# Enter a new book
def add_book():
    global book_id
    book_id += 1        # Auto increment book_ID by 1 to store new record
    new_id = book_id
    new_title = input("Title of the new book: ")
    new_author = input("Author of the new book: ")
    new_qty = input("Quantity of the new book: ")
    
    # Catch exception if duplicate combination of Title and Author is being inserted into table
    try:
        cursor.execute(''' INSERT INTO books ('id', 'Title', 'Author', 'Qty') 
            VALUES (?, ?, ?, ?)''', (new_id, new_title, new_author, new_qty))
    except sqlite3.IntegrityError:
            print("Book with the same Title and Author already exist in the database.")

    print(f"New book added: \nID: {new_id} \n {new_title} by {new_author} \n Qty: {new_qty}")
    

def update_book(updt_book):
    book_id = updt_book

    cursor.execute(''' SELECT id, Title, Author, Qty FROM books WHERE id = ? ''', (book_id,))
    curs = cursor.fetchone()
    # Return to main menu if ID does not exist
    if curs == None:
        print("ID does not exist.")
        return
    else:
        pprint(curs)     

    action = input("Would you like to update 'Title', 'Author' or 'Qty'?").lower()
    
    # Catch exception if duplicate combination of Title and Author is being inserted into table
    try:
        if action == 'title':
            new_value = input("Update title to: ")
            cursor.execute('''UPDATE books SET Title = ? WHERE id = ?''', (new_value, book_id))
            print(f"Title has been updated.\n")
        elif action == 'author':
            new_value = input("Update author to: ")
            cursor.execute('''UPDATE books SET Author = ? WHERE id = ?''', (new_value, book_id))
            print(f"Author has been updated.\n")
        elif action == 'qty':
            try:
                new_value = int(input("Update quantity to: "))
            except ValueError:
                print("Not a valid number entered.")
                return
            cursor.execute('''UPDATE books SET Qty = ? WHERE id = ?''', (new_value, book_id))
            print(f"Quantity has been updated.\n")
        else:
            print("Input not recognised.")
            return

    except sqlite3.IntegrityError:
            print("Book with the same Title and Author already exist in the database.")

def delete_book(input_id):
    book_id = input_id

    cursor.execute(''' SELECT id, Title, Author, Qty FROM books WHERE id = ? ''', (book_id,))
    curs = cursor.fetchone()
    # Return to main menu if ID does not exist
    if curs == None:
        print("ID does not exist.")
        return
    else:
        pprint(curs)

    # Delete record
    cursor.execute('''DELETE FROM books WHERE id = ?''', (book_id,))
    print(f"\n{book_id} has been deleted from the table\n")    


def search_book():
    search_term = input('''Would you like to search by:
    id - book id
    o - title or author
    q - query quantity
    ''')

    if search_term == 'o':
        search_term = input("Please enter book title or author to search the database: ").lower()

        cursor2 = cursor.execute(''' SELECT id, Title, Author, Qty FROM books
                    WHERE Title LIKE ? OR Author LIKE ? ''', (search_term, search_term))
        for row in cursor2.fetchall():
            print(f'{row[0]:<5} : {row[1]:<45s} : {row[2]:<20s} : {row[3]:<3}')
    elif search_term == 'id':
        book_id = input("Please enter the book id to search: ")
        cursor.execute(''' SELECT id, Title, Author, Qty FROM books WHERE id = ? ''', (book_id,))
        curs = cursor.fetchone()
        # Return to main menu if ID does not exist
        if curs == None:
            print("ID does not exist.")
            return
        else:
            pprint(curs)
    elif search_term == 'q':
        qty_1 = int(input("Search books with Qty starting FROM : "))
        qty_2 = int(input("Search books with Qty UP TO : "))
        cursor2 = cursor.execute(''' SELECT id, Title, Author, Qty FROM books
                WHERE Qty BETWEEN ? AND ?''', (qty_1, qty_2))
        for row in cursor2.fetchall():
            print(f'{row[0]:<5} : {row[1]:<45s} : {row[2]:<20s} : {row[3]:<3}')
    else:
        print("Input not recognised.")
        return


# Print all attributes in table
def view_table():
    cursor2 = cursor.execute(''' SELECT id, Title, Author, Qty FROM books''')
    print(f"\nbooks table:")
    
    # f string format alignment. ---- (variable) :<20 ----
    # Take all before : and format it as, < left align, leave 20 char spaces, s because it's a string.
    
    print(f'{"ID":<5s}   {"Title":<45s}   {"Author":<20s}   {"Qty":<3s}')
    for row in cursor2.fetchall():
        print(f'{row[0]:<5} : {row[1]:<45s} : {row[2]:<20s} : {row[3]:<3}')


# Main menu
while logged_in:
    menu = input('''\nPlease select one of the following Options below:

    a - Enter a new book
    u - Update an existing book
    d - Delete an existing book
    s - Search books
    v - View the database
    e - Exit

Option selected : ''').lower()

    if menu == 'a':
        add_book()
    elif menu == 'u':
        input_id = input("Please enter the ID of the book you would like to update: ")
        update_book(input_id)
    elif menu == 'd':
        input_id = input("Please enter the ID of the book you would like to update: ")
        delete_book(input_id)
    elif menu == 's':
        search_book()
    elif menu == 'v':
        view_table()
    elif menu == 'e':
        db.close()      # Close the db connection
        print("Goodbye!!!")
        exit()
    else:
        print("Input not recognised. Please Try again\n")


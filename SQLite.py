'''
SQL Relational Databases with SQLite
Elinore Wright
'''

import sqlite3

connection = sqlite3.connect('library.db')
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS library ( title TEXT, author TEXT, last_read TEXT)")

#credit to Chad Macbeth
#this function is based on his get_name()
def get_title(cursor):
    cursor.execute("SELECT title FROM library")
    results = cursor.fetchall()
    if len(results) == 0:
        print("No title in database")
        return None
    for i in range(len(results)):
        print(f"{i+1} - {results[i][0]}")
    choice = 0
    while choice < 1 or choice > len(results):
        choice = int(input("Title ID: "))
    return results[choice-1][0]

def main():
    choice = None
    #create a while loop that runs until option 6 is chosen 
    while choice != '6':
        print('1. Display books in library ')
        print('2. Add a book')
        print('3. Remove a book')
        print('4. Update a Last Read')
        print('5. Clear all entries')
        print('6. Exit')

        choice = input('Select: ')
        print()

        #Display entries
        if choice == '1':
            cursor.execute('SELECT * FROM library ORDER BY author')
            print(f"{'Title':20} {'Author':20} {'Last Read':20}")
            for book in cursor.fetchall():
                print(f"{book[0]:20} {book[1]:20} {book[2]:20}")

        #Add new entry
        elif choice == '2':
            try:
                title = input('Title: ')
                author = input('Author: ')
                last_read = input('Last Read: ')
                values = (title, author, last_read)
                cursor.execute('INSERT INTO library VALUES (?,?,?)', values)
                connection.commit()
            except ValueError:
                print('Invalid')
        
        #Delete entry
        elif choice == '3':
            title = get_title(cursor)
            if title == None:
                continue
            values = (title, )
            cursor.execute('DELETE FROM library WHERE title = ?', values)
            connection.commit()
            
        #Update entry
        elif choice =='4':
            try:
                title = get_title(cursor)
                if title == None:
                    continue
                last_read = input('Last Read: ')
                values = (last_read, title)
                cursor.execute('UPDATE library SET last_read = ? WHERE title = ?', values)
                connection.commit()
            except ValueError:
                print('Invalid date')
        
        #Clear all entries
        elif choice == '5':
            cursor.execute('DROP TABLE library')
            connection.commit()
            #allows users to continue using the program after dropping the table. Before you had to restart the program
            cursor.execute("CREATE TABLE IF NOT EXISTS library ( title TEXT, author TEXT, last_read TEXT)")

        print()

    #you have to close the connection to the database
    connection.close()

main()
print('See you next time!')

import sqlite3
import time
print("PHONEBOOK_APP")
# making a connection to existing db or creating new db
connection = sqlite3.connect('Phonebook.db')
# creating a cursor class obj
crsr = connection.cursor()
# try to execute table creation (PRIMARY KEY may be used)
try:
    cmd = """CREATE TABLE phonebook (fname VARCHAR(30), lname VARCHAR(30), phone VARCHAR(15), email VARCHAR(40), comment VARCHAR);"""
    crsr.execute(cmd)
except sqlite3.OperationalError:
    print('Table already exist, continue with existing one')

columns = ['name', 'last name name', 'phone number', 'email aderss', 'commentary']


def add():
    row = []
    for column in columns:
        row.append(input(f"Enter {column}: "))
    print('Input:', row)
    cmd = """INSERT INTO phonebook (fname, lname, phone, email, comment) VALUES (?, ?, ?, ?, ?)"""
    crsr.execute(cmd, row)
    print('Item added.')


def utility_search():
    """Search item in db"""
    search = input("find: ")
    cmd = f"""SELECT rowid, * FROM phonebook WHERE fname LIKE '%{search}%' OR lname LIKE '%{search}%' OR phone LIKE '%{search}%' OR email LIKE '%{search}%';"""
    crsr.execute(cmd)
    ans = crsr.fetchall()
    return ans


def utility_print(selected):
    for row in selected:
        print(*row)


def find():
    """Input any text or number to find any full or partial overlap
    in first name, last name, phone number or email adress
    or press Enter to show all items"""
    print('Find items')
    ans = utility_search()
    if not ans:
        print('Nothing found')
        return
    utility_print(ans)


def delete():
    """Input any text or number to find any full or partial overlap
        in first name, last name, phone number or email address
        and than delete the tuple by selecting ID numbers
        or type 0 to return"""
    print('Delete items')
    ans = utility_search()
    if not ans:
        print('Nothing found')
        return
    utility_print(ans)
    while True:
        try:
            erase = list(map(int, input("Enter IDs to delete items. Use space as a separator\n").split()))
        except ValueError:
            print('Try again. Enter IDs to delete items. Use space as a separator\n')
            continue
        break
    for i in erase:
        cmd = f"""DELETE FROM phonebook WHERE rowid = {i}"""
        crsr.execute(cmd)
    print('Items deleted.')


def update():
    """Fine and update one item at a time"""
    print('Update item')
    ans = utility_search()
    if not ans:
        print('Nothing found')
        return
    utility_print(ans)
    while True:
        try:
            upd = (int(input("Enter ID to update item or type 0 to quit: ")))
            if upd == 0:
                print('Returning')
                return
        except ValueError:
            print('Try again. Enter ID to update item or type 0 to quit: ')
            continue
        break

    cmd = f"""SELECT rowid, * FROM phonebook WHERE rowid = {upd};"""
    crsr.execute(cmd)
    item = crsr.fetchall()
    print("Old item:", *item)
    new_input = []
    for column in columns:
        new_input.append(input(f"Enter new {column}: "))

    cmd = f"""UPDATE phonebook SET fname = '{new_input[0]}', lname = '{new_input[1]}', phone = '{new_input[2]}', email = '{new_input[3]}', comment = '{new_input[4]}' WHERE rowid = '{upd}';"""
    crsr.execute(cmd)
    print("Item updated.")


def e():
    """Save changes and quit program"""
    print('Changes have been saved. Quiting.')
    # commit the connection to save changes to database
    connection.commit()
    # close connection at the end
    connection.close()
    time.sleep(5)
    quit()


def cancel():
    """Discard changes and quit program"""
    print("Quiting without saving.")
    connection.close()
    time.sleep(5)
    quit()


def save():
    """Save changes and continue"""
    print("Saving changes")
    connection.commit()


# INSERT value into created table
# cmd = """INSERT INTO phonebook (fname, lname, phone, email) VALUES ("Alice", "McCarthy", "+77777", "bojack@bojackmail.com");"""
# crsr.execute(cmd)


available_functions = {'add': add, 'delete': delete, 'find': find, 'update': update, 'save': save, 'cancel': cancel,
                       'exit': e}
while True:
    time.sleep(0.6)
    print()
    print("""Type 'find' to find an item, 'add' to add an item, 'delete' to delete an item,
'update' to update an item, 'save' to save changes,
'exit' to save changes and exit, 'cancel' to quit without saving changes.""")
    foo = input("Type a command: ")
    if foo not in available_functions:
        print("This command doesn't exist. Try again.")
        continue
    else:
        available_functions[foo]()

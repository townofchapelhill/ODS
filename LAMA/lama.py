# import packages and libraries
import pyodbc
import traceback
import secrets

# connect to LAMA database with username and password
def connect():
    print("connecting...")
    cnxn = pyodbc.connect('driver={ODBC Driver 13 for SQL Server};server=LAMASQL.townofchapelhill.org;database=LAMA;uid=secrets.lamausername;pwd=secrets.lamapassword')
    print("connected.")
    cnxn.setencoding('utf-8')
    return cnxn

# call specified query
def query(cnxn):
    cursor = cnxn.cursor()
    script = ("permits.sql")
    scriptlines = script.readlines()
    print("querying...")
    cursor.execute(scriptlines)
    row = cursor.fetchone()
    print("fetching rows...")
    while row:
        print(row[0])
        row = cursor.fetchone()

# call functions
def main():
    cnxn = connect()
    query(cnxn)

# call main
try:
    print("calling main function...")
    main()
    print("main function successfully called.")
# handle errors and exceptions
except:
    errorlog = open("lamaerror.txt", 'a')
    errorlog.write(traceback.format_exc() + "\n")

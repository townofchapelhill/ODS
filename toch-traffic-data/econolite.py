import pymssql
# writefile = open("detectorLogs.csv", "w")
conn = pymssql.connect(server=secrets.host, user=secrets.username, password=secrets.password, database=secrets.db)
cursor = conn.cursor()

cursor.execute("SELECT * FROM secrets.table_name WHERE Timestamp >= '2018-07-31 00:00:00';")
row = cursor.fetchall()

with open('//CHFS/Shared Documents/OpenData/datasets/staging/econolite.csv', "w") as writefile:
    for item in row: 
        for element in list(item):
            try:
                print(element)
                writefile.write(str(item[0]) + ", " )
                writefile.write(str(item[1]) + ", " )
                writefile.write(str(item[2]) + ", " )
                writefile.write(str(item[3]) + ", " )
                writefile.write(str(item[4]) + ", " )
                writefile.write(str(item[5]) + ", " )
                writefile.write(str(item[6]) + ", " )
                writefile.write(str(item[7]) + "\n " )
                except:
                    continue
   
conn.close()
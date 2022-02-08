import sqlite3


def load_flatmates_date_to_db(flatmates_house_info,labels):
    connection = sqlite3.connect('flatmates_data.db')
    cursor = connection.cursor()
    insert_row_to_db = []
    print(flatmates_house_info)
    for i in labels:
        insert_row_to_db.append(flatmates_house_info[i])

    cursor.execute("INSERT INTO flatmates_rent_listings VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", insert_row_to_db)
    # remove last ,
    #print(flatmates_house_info)
    connection.commit()
    connection.close()


#INSERT INTO TABLE_NAME [(column1, column2, column3,...columnN)]  
#VALUES (value1, value2, value3,...valueN);

#cursor.execute("CREATE TABLE flatmates_house_data(id TEXT, url TEXT, suburb TEXT, city TEXT" +
#               ", price INTEGER, price_includes_bills BOOL, rooms_available INTEGER,"+
#               "house_type TEXT, bedroom_count INTEGER, bathroom_count INTEGER," +
#               "people_count INTEGER, date INTEGER)")


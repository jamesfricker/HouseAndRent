"""file for loading data in sqlite db"""
import sqlite3


def load_flatmates_data_to_db(flatmates_house_info,labels):
    """load data in sqlite database"""
    connection = sqlite3.connect('flatmates_data.db')
    cursor = connection.cursor()
    insert_row_to_db = []
    for i in labels:
        insert_row_to_db.append(flatmates_house_info[i])

    # update
    cursor.execute("UPDATE flatmates_rent_listings " +
                    "SET date=date " +
                    "WHERE flatmates_id='" +str(flatmates_house_info["flatmates_id"]) + "';")
    try:
        cursor.execute("INSERT OR IGNORE INTO flatmates_rent_listings " +
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", insert_row_to_db)
        print("Successfully insert or updated listing " +
            str(flatmates_house_info["flatmates_id"]) + " into db")
    except Exception:
        print("Error inserting listing " + str(flatmates_house_info["flatmates_id"]) + " into db")

    connection.commit()
    connection.close()
    
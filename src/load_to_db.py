"""file for loading data in sqlite db"""
import sqlite3
import os
import csv


def load_flatmates_data_to_db(flatmates_house_info, labels):
    """load data in sqlite database"""
    connection = sqlite3.connect("src/db/flatmates_data.db")
    cursor = connection.cursor()
    insert_row_to_db = []
    for i in labels:
        insert_row_to_db.append(flatmates_house_info[i])

    # update
    cursor.execute(
        f"""
    UPDATE flatmates_rent_listings
    SET date=date
    WHERE flatmates_id='{str(flatmates_house_info["flatmates_id"])}';
    """
    )
    try:
        cursor.execute(
            """
        INSERT OR IGNORE INTO flatmates_rent_listings
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """,
            insert_row_to_db,
        )
        print(
            "Successfully insert or updated listing "
            + str(flatmates_house_info["flatmates_id"])
            + " into db"
        )
    except Exception as exception:
        print(
            "Error inserting listing "
            + str(flatmates_house_info["flatmates_id"])
            + " into db"
            + str(exception)
        )
    connection.commit()
    connection.close()


def read_csv_extract():
    """read csv file and extract data"""
    output_location = os.path.join(os.getcwd(), "output")
    print(output_location)
    files = os.listdir(output_location)
    files.sort()
    latest_extract = files[-1]
    print(latest_extract)
    return csv.DictReader(open(f"output/{latest_extract}", "r", encoding="utf-8"))


if __name__ == "__main__":
    output_reader = read_csv_extract()
    for row in output_reader:
        load_flatmates_data_to_db(row, output_reader.fieldnames)
    print("finished loading data to db")

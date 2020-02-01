import sqlite3
import json
import alphavantageAPIcall as aAPI
from urllib.request import urlretrieve


def get_new_MACD_file(json_file):
    url = aAPI.call_MACD('SPY', '60min', 'json')
    urlretrieve(url, json_file)


def create_db_from_json(json_file, table_name, conn):
    c = conn.cursor()
    with open(json_file) as j:
        data = json.load(j)
    head_titles = ""
    head_complete = 0
    for key1 in data:
        if not key1 == 'Meta Data':
            for key in data[key1]:
                if head_complete == 0:
                    for key2 in data[key1][key]:
                        head_complete = 1
                        if head_titles == "":
                            head_titles = "'Time_Stamp', '" + key2 + "'"
                        else:
                            head_titles = head_titles + ", '" + key2 + "'"
    sql_create = "CREATE TABLE " + table_name + " (" + head_titles + ")"
    c.execute(sql_create)


def populate_db_from_json(json_file, table_name, conn):
    c = conn.cursor()
    with open(json_file) as j:
        data = json.load(j)
    for key1 in data:
        if not key1 == 'Meta Data':
            for key in data[key1]:
                record_str = "'" + key + "'"
                for key2 in data[key1][key]:
                    record_str = record_str + ", '" + data[key1][key][key2] + "'"
                sql_insert = "INSERT INTO " + table_name + " VALUES (" + record_str + ")"
                c.execute(sql_insert)
                conn.commit()


def add_new_records_to_db(table_name, conn):  # Adds records from the newest json file into the main database table
    c = conn.cursor()
    sql_insert2 = "INSERT INTO spyMACD SELECT * FROM " + table_name +" WHERE " + table_name + ".Time_Stamp NOT IN (" \
                                                                                              "SELECT Time_Stamp FROM" \
                                                                                              " spyMACD) "
    c.execute(sql_insert2)
    conn.commit()
    sql_drop = "DROP TABLE " + table_name
    c.execute(sql_drop)
    conn.commit()
    sql_orderby = "SELECT * FROM spyMACD ORDER BY Time_Stamp DESC"
    c.execute(sql_orderby)
    conn.commit()


def main():
    db_filepath = 'testfile.json'  # 'testfile1.json'
    get_new_MACD_file(db_filepath)
    db_table_name = 'temp1'  # 'spyMACD'
    conn = sqlite3.connect('spyMACD.db')
    create_db_from_json(db_filepath, db_table_name, conn)
    populate_db_from_json(db_filepath, db_table_name, conn)
    add_new_records_to_db(db_table_name, conn)


if __name__ == '__main__':
    main()

import sqlite3
import json


def table_col(database_file, output_file):
    
    #creating a connection with sqlite database
    conn = sqlite3.connect(database_file)
    Hand = conn.cursor()
    
    #getting all the table names from the database file
    Hand.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = Hand.fetchall()
    table_columns = {}
    
    #fetching the table to get column names
    for tab in tables:
        table_name = tab[0]
        Hand.execute(f"PRAGMA table_info({table_name});")
        col = Hand.fetchall()
        table_columns[table_name] = [column[1] for column in col]
    conn.close()
    Final_data = {}
    for table, columns in table_columns.items():
        conn = sqlite3.connect(database_file)
        Hand = conn.cursor()
        
        #fetching the current table and column to get data row by row
        Hand.execute(f"SELECT {', '.join(columns)} FROM {table};")
        data = Hand.fetchall()
        
        #creating a list of dictionaries from above fetched data
        res = []
        for row in data:
            res.append(dict(zip(columns, row)))    
        Final_data[table] = res
        conn.close()
        
        #converting the data to get row by row records
        rec_row = []
    for i in range(len(res)):
        rec = {}
        for tab, data in Final_data.items():
            if i < len(data):
                rec[tab] = data[i]
        rec_row.append(rec)
        
        #finally saving the records as JSON format in output file
    with open(output_file, 'w') as json_file:
        json.dump(rec_row, json_file, indent=2)

database_file = "cma-artworks.db"
output_file = "artworks.txt"
table_col(database_file, output_file)

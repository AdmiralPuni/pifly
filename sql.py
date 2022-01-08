import os
import json
import time
import sqlite3
from tqdm import tqdm

connection = sqlite3.connect('database/noflies.db', check_same_thread=False)
#connection = sqlite3.connect('database/noflies.db')

def current_time_iso():
  return time.strftime("%Y-%m-%dT%H-%M-%SZ", time.localtime(time.time()))

def create_table():
  connection_cursor = connection.cursor()
  connection_cursor.execute("""CREATE TABLE devices(
    id TEXT PRIMARY KEY,
    battery TEXT,
    water_level TEXT,
    radar INTEGER,
    occupied INTEGER
  )
  """)
  connection_cursor.close()

def update_field(field, value, id):
  connection_cursor = connection.cursor()
  connection_cursor.execute("UPDATE devices SET " + field + "=? WHERE id=?", (value, id))
  connection_cursor.close()
  connection.commit()

def reset_database():
  connection_cursor = connection.cursor()
  connection_cursor.execute("DROP TABLE devices")
  connection_cursor.close()
  create_table()

def select_all_device():
  connection_cursor = connection.cursor()
  connection_cursor.execute("SELECT * FROM devices")
  return connection_cursor.fetchall()

def select_single_device(id):
  connection_cursor = connection.cursor()
  connection_cursor.execute("SELECT * FROM devices WHERE id=?", (id,))
  return connection_cursor.fetchall()

def insert_new_device(id):
  connection_cursor = connection.cursor()
  connection_cursor.execute("INSERT INTO devices VALUES (?, ?, ?, ?, ?)", (id, '', '', 0, 0))
  connection_cursor.close()
  connection.commit()

def delete_device(id):
  connection_cursor = connection.cursor()
  connection_cursor.execute("DELETE FROM devices WHERE id=?", (id,))
  connection_cursor.close()

def select_device_id():
  connection_cursor = connection.cursor()
  connection_cursor.execute("SELECT id FROM devices")
  #return the result to a listr
  id_list = []
  data = connection_cursor.fetchall()
  for row in data:
    id_list.append(row[0])
  return id_list

def main():
  print(select_device_id())
  #return
  reset_database()
  insert_new_device('A')
  insert_new_device('B')
  insert_new_device('C')
  connection.commit

if __name__ == '__main__':
  main()

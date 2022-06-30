import csv
from models.device import device
import time
import datetime
import os

FILE_NAME = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + ".csv"
FILE_PATH = "static/experiment/"

#if file does not exist, create it
if not os.path.isfile(FILE_PATH + FILE_NAME):
  with open(FILE_PATH + FILE_NAME, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['serial_number', 'name', 'battery', 'water', 'radar', 'interval', 'timestamp'])

def log(data):
  #append data to csv file
  with open(FILE_PATH + FILE_NAME, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

def main():
  while True:
    print("LOGGING DATA AT           " + datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S"))
    try:
      data = []
      raw = device.get_test_by_email('latency@gmail.com')
      for row in raw:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        data.append([row['serial_number'], row['name'], row['battery'], row['water'], row['radar'], row['interval'], timestamp])
      log(data)
    except Exception as e:
      print(e)

    print("COMPLETED LOGGING DATA AT " + datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S"))

    #wait for an hour
    time.sleep(3600)

if __name__ == '__main__':
  main()
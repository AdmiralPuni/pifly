import csv
import numpy as np
from matplotlib import pyplot as plt

#CSV_FILE = 'BBLATENCY2022-06-30T12-25-40.csv'
CSV_FILE = '1WAYLATENCY2022-06-30T12-25-36.csv'
UNIQUE_NAMES = ['MONA', 'LISA', 'BOSSA', 'NOVA', 'TERRA', 'COTA']
data = {}

#init data
for name in UNIQUE_NAMES:
  data[name] = []

def get_data():
  global data
  with open(CSV_FILE, 'r') as csvfile:
    reader = csv.reader(csvfile)
    #remove first row
    next(reader)
    for row in reader:
      #col 1 is name, 2 is latency
      data[row[0]].append(float(row[1]))

def plot_data():
  #copy data to local_data
  local_data = {}
  for name in UNIQUE_NAMES:
    local_data[name] = data[name]
  #only get data 100-300
  for name in UNIQUE_NAMES:
    local_data[name] = local_data[name][100:200]
    plt.plot(local_data[name], label=name)
  #plot data
  plt.legend()
  plt.show()
  

def main():
  global data
  get_data()
  plot_data()
  
  stats = {}
  for name in UNIQUE_NAMES:
    stats[name] = {}
    #round to 3 decimal places
    stats[name]['mean'] = round(np.mean(data[name]), 3)
    stats[name]['std'] = round(np.std(data[name]), 3)
    stats[name]['min'] = round(np.min(data[name]), 3)
    stats[name]['max'] = round(np.max(data[name]), 3)

  #print headers
  print("{:<20}{:<20}{:<20}{:<20}{:<20}".format("Name", "Mean", "Std", "Min", "Max"))

  for name in UNIQUE_NAMES:
    print("{:<20}".format(name), end='')
    for key in stats[name]:
      print("{:<20}".format(stats[name][key]), end='')
    print()
  print()



  return

if __name__ == '__main__':
  main()
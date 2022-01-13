import matplotlib.pyplot as plt
import numpy as np
import csv

device_list = ['NF1', 'NF2']
delays_nf1 = []
delays_nf2 = []

#open csvlatency.csv and read the data
with open('csv/csvlatency.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)


#get the data from the csv file
for i in range(1, len(data)):
    if i == 0:
        continue
    if data[i][1] == 'NF1':
        delays_nf1.append(float(data[i][4]))
    elif data[i][1] == 'NF2':
        delays_nf2.append(float(data[i][4]))

#print the mean, coefficient of variation and standard deviation for each device
print('STATICTIC FOR NF1')
print('Mean:', np.mean(delays_nf1))
print('Coefficient of variation:', np.std(delays_nf1)/np.mean(delays_nf1))
print('Standard deviation:', np.std(delays_nf1))
print('Max delay:', max(delays_nf1))
print('Min delay:', min(delays_nf1))
print('STATICTIC FOR NF2')
print('Mean:', np.mean(delays_nf2))
print('Coefficient of variation:', np.std(delays_nf2)/np.mean(delays_nf2))
print('Standard deviation:', np.std(delays_nf2))
print('Max delay:', max(delays_nf2))
print('Min delay:', min(delays_nf2))


#plot the data
plt.plot(delays_nf1, label='NF1')
plt.plot(delays_nf2, label='NF2')
plt.xlabel('Time')
plt.ylabel('Latency')
plt.title('Latency of the devices')
plt.legend()
plt.show()
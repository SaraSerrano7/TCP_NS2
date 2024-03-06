#!/usr/bin/python3.8

import matplotlib.pyplot as plt

trace_file = "sor.slow7"
#trace_file = "to.slow7.rtt"
trace_data=""


with open(trace_file, 'r') as file:
	trace_data = file.read()

print(trace_data)
lines = trace_data.strip().split('\n')
for line in lines:
	if line[0] == 'd':
		print('dropped')

#print(trace_data)

'''
# Parse the trace data
lines = trace_data.strip().split('\n')
# lines = trace_data_2.strip().split('\n')
time = []
congestion_window = []
for line in lines:
    #print(line)
    t, cwnd = map(float, line.split())
    
    #t, cwnd = line.split()
    #t = float(t)
    #cwnd = float(cwnd)
    	
    time.append(t)
    congestion_window.append(cwnd)

# Plot congestion window over time
plt.plot(time, congestion_window, label='Congestion Window')
plt.xlabel('Time')
plt.ylabel('Congestion Window')
plt.title('Congestion Window Evolution')
plt.legend()
plt.grid(True)
plt.show()
'''

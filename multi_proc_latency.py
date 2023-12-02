#!/usr/bin/python

import random

print("starting up\n")

# All times in real seconds.

start_time = 0
#end_time = 1.0
num_cpus = 16
total=10000
tasks = [None] * total
completions = [None] * total
latencies = [None] * total

task_latency = 0.01
target_utilization = 0.9
end_time = total * task_latency / target_utilization / float(num_cpus)
print ("end time : %s" % end_time)

# Setup tasks
for x in range(0,total):
  tasks[x] = random.uniform(start_time, end_time)
tasks.sort()

time = 0.0
cpu_time = [0] * num_cpus
cpu_idx = 0

idx = 0
for x in tasks:
  # fast-forward time to next task
  time = cpu_time[cpu_idx]
  if x > time:
    time = x
  time += task_latency
  completions[idx] = time
  latencies[idx] = completions[idx] - tasks[idx]
  cpu_time[cpu_idx] = time
  cpu_idx = (cpu_idx + 1) % num_cpus
  idx += 1

# Sort latencies and render results.
latencies.sort()
print ("ideal task latency : %s" % task_latency)
print ("total tasks : %s" % total)
print ("target utilization : %s" % target_utilization)
print ("utilization: %s" % (task_latency*total / num_cpus / (end_time-start_time)))
print ("num_cpus : %s" % num_cpus)


for pct in [0.25,0.50,0.90,0.95,0.99]:
  pct_latency = latencies[int(pct*total)]
  print ("latency at %0.2f pct: %0.6f" % (pct, pct_latency))
  print ("    mult factor: %2.1f" % (pct_latency / task_latency))

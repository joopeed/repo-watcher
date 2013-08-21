import subprocess
from experiment_library import *

with open('machines', 'r') as machine_data:
	machines = read_machines(machine_data)

for component, ip_list in machines.items():
	for actual_ip, local_actual_ip in ip_list:
		# Clean each machine by stopping the components and erasing the paths
		kill_others(component, actual_ip)
		execute_with_sudo("rm -r /mnt/*", actual_ip)
		execute_with_sudo("rm -r /home/ubuntu/*", actual_ip)



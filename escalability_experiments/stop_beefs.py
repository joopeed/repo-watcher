import subprocess
from experiment_library import *
with open('machines', 'r') as machine_data:
	machines = read_machines(machine_data)

for component, ip_list in machines.items()[::-1]:
	for actual_ip, local_actual_ip in ip_list:
		execute_with_sudo("bash /mnt/super/bin/beefs stop "+component, actual_ip)
		kill_others(component, actual_ip)
		execute_with_sudo("rm -r /mnt/Queenbee*", actual_ip)
		execute_with_sudo("rm -r /mnt/Honeybee*", actual_ip)
		execute_with_sudo("rm -r /mnt/Honeycomb*", actual_ip)
		execute_with_sudo("rm -r /mnt/storage/*", actual_ip)
		execute_with_sudo("rm -r /tmp/result.txt", actual_ip)



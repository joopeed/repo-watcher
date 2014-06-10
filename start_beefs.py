import subprocess, experiment_library
from experiment_library import *
with open('machines', 'r') as machine_data:
	machines = read_machines(machine_data)

machines_ignored = []
machines_running = []
num = 0

for component, ip_list in machines.items():
	for actual_ip, local_actual_ip in ip_list:

		if component=="combee": num+=1 # counts the number of combees

		execute_with_sudo("bash /mnt/super/bin/beefs start "+component, actual_ip) # starts beefs
		if not component_is_running(component, actual_ip) or not mountpoint_is_actually_mounted(actual_ip): 
			machines_ignored.append(actual_ip) # If there was any error while starting beefs, the machine is ignored
			num-=1
		else: 
			machines_running.append([actual_ip, local_actual_ip, component]) # If not, then it will be useful
		
		execute_with_sudo("mkdir /mnt/beefs/test_place", actual_ip) # creates a path into the mount point
		execute_with_sudo("chown ubuntu /mnt/beefs/test_place", actual_ip) # which one will receive the files

for i in range(num):
	# Creates based on the quantity of combees running beefs, paths to each combee copy its files
	# This way we ensure that a combee wont overwrite another while copying a file
	execute_with_sudo("mkdir /mnt/beefs/test_place/place"+str(i), actual_ip)	



print str(len(machines_ignored)) + " machines were ignored because could not run the BeeFS ( below is the list of them ),\n "
	+ str(len(machines_running))+" are running BeeFS right now"

print "Ignored Machines"
for ip in machines_ignored:
	print ip

# The file "machines_running_beefs" will be useful while collecting the results
script = open("machines_running_beefs", "w")
for machine_info in machines_running:
	script.write(" ".join(machine_info)+"\n")
script.close()

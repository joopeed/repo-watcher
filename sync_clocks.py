from experiment_library import *
from time import sleep
	
def sync_clock(actual):
	# Synchronizes the clock of the actual machine
	execute("sudo ntpdate ntp.pop-pb.rnp.br", actual)


with open('machines', 'r') as machine_data:
	machines = read_machines(machine_data)

for component, ip_list in machines.items():
	for actual_ip, local_actual_ip in ip_list:
		print "Sychronizing clock of "+ actual_ip
		sync_clock(actual_ip)


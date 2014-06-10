import subprocess
from time import sleep
from experiment_library import *

def config_hostname(machines, actual_ip, local_actual_ip):
	# Configures the /etc/hosts of all machines 
	# The actual machine receives the localhost ip (127.0.0.1)
	actual_hostname = "ii"
	etchosts = ""
	for component, ip_list in machines.items():
		for i in range(len(ip_list)):
			ext_actual_ip, local_actual_ip = ip_list[i]
			hostname = component + "-" + str(i) 
			if not actual_ip == ext_actual_ip:
				etchosts += local_actual_ip + " " + hostname +"\n"
			else:
				etchosts += "127.0.0.1" + " " + hostname +"\n"
				actual_hostname  = hostname

	etchosts += """
# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters""" 
	#print out, err, code
	execute_with_sudo("echo '"+etchosts+"' > /etc/hosts", actual_ip)
	execute_with_sudo("echo '"+actual_hostname+"' > /etc/hostname", actual_ip)
	execute_with_sudo("reboot now", actual_ip)
	sleep(40)

def update_and_install_libs(actual):
	# Updates the package lists and installs java that is needed to run BeeFS
	execute("sudo apt-get -y update", actual)
	execute("sudo apt-get -y install openjdk-7-jdk openjdk-7-jre unzip python", actual)
		
def sync_clock(actual):
	# Synchronizes the clock of the actual machine
	execute("sudo ntpdate ntp.pop-pb.rnp.br", actual)



with open('machines', 'r') as machine_data:
	machines = read_machines(machine_data)

for component, ip_list in machines.items():
	for actual_ip, local_actual_ip in ip_list:
		print "Configuring the hostname for "+ actual_ip
		config_hostname(machines, actual_ip, local_actual_ip)
		print "Updating and installing libraries for "+ actual_ip
		update_and_install_libs(actual_ip)
		print "Sychronizing clock of "+ actual_ip
		sync_clock(actual_ip)


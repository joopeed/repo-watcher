import ConfigParser, subprocess
from experiment_library import *

conf = {}
config = ConfigParser.ConfigParser()
config.readfp(open('enviroment'))
for troco, valor in config.items("General"):
	conf[troco] = valor

with open('machines', 'r') as machine_data:
	machines = read_machines(machine_data)


for component, ip_list in machines.items():
	for actual_ip, local_actual_ip in ip_list:
		execute_with_sudo("chmod 777 /mnt", actual_ip)
		print "Copying beefs.zip to "+actual_ip
		copy_file(conf["beefs_zip_path"], actual_ip)	
		print "Copying workload.zip to "+actual_ip
		copy_file(conf["workload_zip_path"], actual_ip)
		print "Unzipping beefs.zip to "+actual_ip
		execute_with_sudo("mkdir /mnt/super", actual_ip)
		execute_with_sudo("unzip -x -o -d /mnt/super /mnt/super.zip ", actual_ip)
		execute_with_sudo("rm -r /mnt/workload", actual_ip)
		execute_with_sudo("mkdir /mnt/workload", actual_ip)
		execute_with_sudo("unzip -x -o -d /mnt/workload /mnt/workload.zip ", actual_ip)
		print "Making directories needed to run BeeFS"
		execute_with_sudo("rm -r /mnt/storage", actual_ip)
		execute_with_sudo("mkdir /mnt/storage", actual_ip)
		execute_with_sudo("rm -r /mnt/beefs", actual_ip)
		execute_with_sudo("mkdir /mnt/beefs", actual_ip)	
		
	

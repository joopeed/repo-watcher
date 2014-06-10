import subprocess
from time import sleep

PASSWORD = "joopeedsLSD123"
DEFAULT_MOUNT_POINT = "/mnt"
USER = "ubuntu"
KEY = "mykey.private"

def execute(remote_command, machine_addr = None):
		# Executes the command remotely or not
		if machine_addr is not None:
			cmd = "sshpass -p "+ PASSWORD +" ssh "+USER+"@"+machine_addr+" "+remote_command
		else:
			cmd = remote_command
    		process = subprocess.Popen(cmd,
					 shell=True,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT)
   		out, err = process.communicate()
		print out
    		return out, err, process.returncode

def execute_with_sudo(remote_command, machine_addr):
		# Executes the commands with sudo.
		# The sudo is not allowed by argument in the ssh command
		# So the command is copied like a file and executed by calling this file with sudo
		def copy_script(path, actual_ip):
			cmd = "sshpass -p "+ PASSWORD +" scp "+path+" "+USER+"@"+actual_ip+":/home/ubuntu"
			process = subprocess.Popen(cmd,
					 shell=True,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT)
			   			
			out, err = process.communicate()
			print out
    			return out, err, process.returncode

		script = open("tmp.sh", "w")
		print remote_command
		script.write(remote_command+"\n")
		script.close()
		copy_script("tmp.sh", machine_addr)
		execute("sudo bash tmp.sh",machine_addr)
		execute("rm tmp.sh", machine_addr)

def read_machines(machines_data):
	# Reads the machine_file and gives a name to each component 
	# If there are two Combees, the first read will 
	# be combee-0, the second, combee-1 and so on
	machines = {}
	for line in machines_data:
		ip, local_ip, iden = line.split()
		if iden in machines:
			machines[iden].append((ip, local_ip))
		else:
			machines[iden] = [(ip, local_ip)]
	return machines



def kill_others(component, actual_ip):
	# Kill all others components running at the machine
	out, err, rcod = execute("ps xau | grep " +  component.capitalize() + " | grep root | grep -v grep", actual_ip)
	if "port 22: No route to host" in out:
		print actual_ip+" doesn't respond"
		return False
	if out.split()!=[]:
		print "There is another instance of "+component+" running on "+actual_ip
		print "Killing now... Process "+out.split()[1]
		execute_with_sudo("kill "+out.split()[1], actual_ip)	
		return True
			

def copy_file(file_path, actual):
	# Copies any file to the the "actual" machine
	cmd = "sshpass -p "+ PASSWORD +" scp -r "+file_path+" "+USER+"@"+actual+":" + DEFAULT_MOUNT_POINT
	file_name = file_path.split("/")[-1]
	process = subprocess.Popen(cmd,
					 shell=True,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT)
   	out, err = process.communicate()
    	return out, err, process.returncode



def component_is_running(name, actual_ip):
	# Waits for 5 seconds and then verifies if the component is actually running
	sleep(5)
        out, err, rcod = execute("ps xau | grep " + 
                              	   	name.capitalize() + 
                                 	 " | grep root | grep -v grep", actual_ip)
      	return out #if it is running, out is not empty, so it's is true

def mountpoint_is_actually_mounted(actual_ip):
	# Verifies if the mount point is actually mounted
        out, err, rcod = execute("df" + 
         " | grep " + DEFAULT_MOUNT_POINT + "beefs | grep -v grep", actual_ip)
	return out #if it is running, out is not empty, so it's is true


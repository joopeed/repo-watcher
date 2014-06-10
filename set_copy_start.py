import subprocess, datetime, ConfigParser
from experiment_library import *

with open('machines_running_beefs', 'r') as machine_data:
	machines = read_machines(machine_data)

conf = {}
config = ConfigParser.ConfigParser()
config.readfp(open('enviroment'))
for troco, valor in config.items("General"):
	conf[troco] = valor

now = datetime.datetime.now() 
copy_start_time = now + datetime.timedelta(minutes=int(conf["minutes_until_start_copying"])) + datetime.timedelta(hours=3) # +3 because UTC+3
copy_start_time_formatted = str(copy_start_time.day)+"/"+str(copy_start_time.month)+"/"+ str(copy_start_time.year)+" "+str(copy_start_time.hour)+":"+str(copy_start_time.minute)


for component, ip_list in machines.items():
	for i in range(len(ip_list)):
		# For each machine, it sets the same time to start copying
		actual_ip, local_actual_ip = ip_list[i]
		commands = """
import time, subprocess, sys, datetime
command = "cp -r /mnt/workload/* /mnt/beefs/test_place/place"""+str(i)+"""" 
while True: 
	if datetime.datetime.now() >= datetime.datetime.strptime('"""+copy_start_time_formatted+"""', "%d/%m/%Y %H:%M"): break
startepoch = int(time.time())
process = subprocess.Popen(command,
			shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
out, err = process.communicate()
endepoch = int(time.time())
print datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
print endepoch - startepoch

"""		
		script = open("copy.py", "w")
		script.write(commands)
		script.close()
		copy_file("copy.py", actual_ip)
		execute_with_sudo("nohup python /mnt/copy.py > /tmp/result.txt &", actual_ip)



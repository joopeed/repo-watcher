from experiment_library import *
import datetime, ConfigParser, sys

with open('machines', 'r') as machine_data:
	machines = read_machines(machine_data)

# Gets from argv the execution turn.
# The experiment may be executed more than once, this way you can name each turn
turn = sys.argv[1]

conf = {}
config = ConfigParser.ConfigParser()
config.readfp(open('enviroment'))

# For each variable in the configuration file it attributes a value
for variable, value in config.items("General"):
	conf[variable] = value

# For each component, gets the ip_list
for component, ip_list in machines.items():
	# The ip list keeps two ips of the component. 
	# That could be useful if you have a machines that are only accessible from the local network
	# The script may be adapted to the situation
	for actual_ip, local_actual_ip in ip_list:
		quant = len(ip_list)	
		print "Collecting results from "+ actual_ip
		execute("sshpass -p joopeedsLSD123 scp ubuntu@"+actual_ip+":/tmp/result.txt "+conf["results_path"]+"/"+str(quant)+"machines/"+turn+"/result."+actual_ip+"."+datetime.datetime.now().strftime("_%dd_%mm_%yy_%Hh.%Mmin%Ss")+".txt")





#!/usr/bin/python
# coding: utf-8

import subprocess, os, sys, re, platform, datetime, time, getpass
from time import sleep

so = platform.system()
if so == "Linux":
	sep = '/'
else:
	sep = '\\'
user = "joopeeds"

class Component:
	def __init__(self, name, machine, conf, conf2, zipped_path):
        	self.__name = name
		self.__machine = machine
		self.__confplace = conf
		self.__conf = openconf(conf)
		self.__zipped_path = zipped_path 
		if conf2: 
			self.__conf2 = openconf(conf2)
			self.__conf2place = conf2
		self.identify_SO()			

	def name(self):
        	return self.__name
	
	def conf(self):
        	return self.__conf

	def conf_place(self):
		return self.__confplace

	def conf2(self):
        	return self.__conf2

	def conf2_place(self):
		return self.__conf2place
	
	def so(self):
        	return self.__so.strip("\n").strip("\r")

	def machine(self):
        	return self.__machine

	def zipped(self):
        	return self.__zipped_path.split(sep)[-1]
	
	
	def _get_time(self):
		return datetime.datetime.now().strftime("[%d/%m/%Y %H:%M:%S]-> ")

	def execute(self, remote_command, machine_addr, delay=None):
		if machine_addr is not None:
			cmd = "ssh "+user +"@" + machine_addr+" "+remote_command
		else:
			cmd = remote_command
    		process = subprocess.Popen(cmd,
					 shell=True,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT)
   		out, err = process.communicate()
    		return out, err, process.returncode
	"""
	def execute_on_windows(self, remote_command, machine_addr, delay=None):
		cmd = "ssh "+user +"@" + machine_addr
    		process = subprocess.Popen(cmd,
					 #shell=True,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
		sleep(1)
		process.stdin.write(remote_command+"\n")

	"""
	def start_on_windows(self, remote_command, machine_addr, delay=None):
		if machine_addr is not None:
			cmd = "ssh "+user +"@" + machine_addr
		else:
			cmd = remote_command
    		process = subprocess.Popen(cmd,
					# shell=True,
					stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
		sleep(1)
		process.stdin.write("cd beefs-tester/superzz/bin/\n")
   		process.stdin.write("beefs.bat start "+self.name()+"\n")
    		return out, err, process.returncode
	
	def copy_zip(self, machine, zipped_path):
		# Copy the zip from the path given in test_config.conf
		if self.so()=='Linux':
        		remote_path = user+"@" + machine + ":/tmp/"
        		getdata_cmd = " ".join(["scp", "-r",
        	                        zipped_path,	
        	                        remote_path])
			process = subprocess.Popen(getdata_cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        		out, err = process.communicate()
		else:
			self.execute("unzip -o "+zipped_path+" -d superzz", None)
			self.execute("mkdir C:/beefs-tester/superzz/superzz", machine)
			getdata_cmd = "sftp "+user+"@" + machine
        		process = subprocess.Popen(getdata_cmd,	
                                  shell=True,
				   stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
			process.stdin.write("cd beefs-tester/superzz/\n")
			process.stdin.write("put -r superzz/*\n")
			process.stdin.write("quit\n")
			#print process.stdout.readline()
			out, err = "","" #process.communicate()
        	return out, err, process.returncode

	def copy_workload(self,  machine, workload_path):
		# Copy the zip from the path given in test_config.conf
		if self.so()=='Linux':
        		remote_path = user+"@" + machine + ":/tmp/"
        		getdata_cmd = " ".join(["scp", "-r",
        	                        workload_path,
        	                        remote_path])
			process = subprocess.Popen(getdata_cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        		out, err = process.communicate()
		else:
			self.execute("unzip -o "+workload_path+" -d workloadzz", None)
			self.execute("mkdir C:/beefs-tester/workloadzz/workloadzz", self.machine())
			getdata_cmd = "sftp "+user+"@" + machine
        		process = subprocess.Popen(getdata_cmd,
                                  stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT,stdin=subprocess.PIPE)	
			process.stdin.write("cd beefs-tester/workload/\n")
			process.stdin.write("put -r workloadzz/*\n")
			process.stdin.write("quit\n")
			print process.stdout.readline()
			out, err = "","" #process.communicate()
        	return out, err, process.returncode

	def copy_files(self,  machine, src_path, dest_path):
		# Copy files from a path in this computer to a remote destination
		if self.so()=='Linux':
        		remote_path = user+"@" + machine + ":/"+dest_path
        		getdata_cmd = " ".join(["scp", "-r",
        	                        src_path,
        	                        remote_path])
			process = subprocess.Popen(getdata_cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        		out, err = process.communicate()
		else:
			getdata_cmd = "sftp "+user +"@" + machine
        		process = subprocess.Popen(getdata_cmd,		
                                   stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
			process.stdin.write("cd "+dest_path+"\n")
			process.stdin.write("put -r "+src_path+"\n")
			process.stdin.write("quit\n")
			out, err = "","" 
        	return out, err, process.returncode

    	def mount(self, workload_path):
		if self.so()=="Linux":
			if self.name() in ["honeycomb","queenbee","combee"]:
				print self._get_time()+"Cleaning previous files..."
				
				self.execute("rm -r /tmp/superzz", self.machine())
				self.execute("rm -r /tmp/"+self.zipped(), self.machine())
				self.execute("rm -r /tmp/workloadzz", self.machine())
				self.execute("rm -r /tmp/"+workload_path.split(sep)[-1], self.machine())
				# Copy BeeFS zip
				print self._get_time()+"Copying BeeFS ZIP ("+self.zipped()+") on "+ self.machine()
				self.copy_zip(self.machine(), self.zipped())
				# print self.execute("ls /tmp/", self.machine())
				# Unzip the files of BeeFS
				print self._get_time()+"Unzipping BeeFS ZIP: /tmp/superzz"
				self.execute("unzip /tmp/"+self.zipped()+" -d /tmp/superzz", self.machine())
				# Remove the zip, already unzipped
				print self._get_time()+"Removing Zip..."
				#self.execute("rm /tmp/"+self.zipped(), self.machine())
			if not self.name() == "combee":
				# Copy the configuration file of component in remote machine that will run it
				print self._get_time()+"Copying "+self.name()+".conf files into: tmp/superzz/conf/"+self.name()+".conf"
				self.copy_files(self.machine(), self.conf_place(), "tmp/superzz/conf/"+self.name()+".conf")	

			else:
				# Copy the configuration file of component in remote machine that will run it
				print self._get_time()+"Copying honeycomb.conf files into: tmp/superzz/conf/honeycomb.conf"
				self.copy_files(self.machine(), self.conf_place(), "tmp/superzz/conf/honeycomb.conf")
				# Copy the configuration file of component in remote machine that will run it
				print self._get_time()+"Copying honeybee.conf files into: tmp/superzz/conf/honeybee.conf"
				self.copy_files(self.machine(), self.conf2_place(), "tmp/superzz/conf/honeybee.conf") 
			
		
			if self.name() == "honeycomb" or self.name() == "combee":
				print self._get_time()+"Making directories needed to run BeeFS..."
				self.execute("mkdir "+self.conf()["contributing_storage.directory"], self.machine()) 
			if self.name() == "honeybee" or self.name() == "combee":
				print self._get_time()+"Making directories needed to run BeeFS..."
				if self.name() is "combee":
					self.execute("mkdir "+self.conf2()["mount_directory"], self.machine())
					self.execute("rm -r "+self.conf2()["mount_directory"]+"/*", self.machine())
				else:
					self.execute("mkdir "+self.conf()["mount_directory"], self.machine())
					self.execute("rm -r "+self.conf()["mount_directory"]+"/*", self.machine())
				# Copy workload zip
				print self._get_time()+"Copying workload.zip into /tmp"
				self.copy_workload( self.machine(), workload_path)
				# Unzip the files of workload 
				workload = workload_path.split(sep)[-1]
				print self._get_time()+"Unzipping workload: /tmp/workloadzz"
				self.execute("unzip /tmp/"+workload+" -d /tmp/workloadzz", self.machine())
				# Remove the zip, already unzipped
				self.execute("rm /tmp/"+workload, self.machine())
		else:
			
			print self._get_time()+"Cleaning previous files..."
			self.execute("rm -r C:/beefs-tester/superzz/*", self.machine())
			self.execute("rm -r C:/beefs-tester/workloadzz/*", self.machine())
			# Copy BeeFS zip
			self.execute("mkdir C:/beefs-tester/", self.machine())
			self.execute("mkdir C:/beefs-tester/superzz", self.machine())
			self.execute("mkdir C:/beefs-tester/workloadzz", self.machine())
			print self._get_time()+"Copying BeeFS ZIP ("+self.zipped()+") and extracting... on "+ self.machine()
			self.copy_zip(self.machine(), self.zipped())
			print self._get_time()+"Unzipping BeeFS ZIP: C:/beefs-tester/superzz"
			if self.name() != "combee":
				# Copy the configuration file of component in remote machine that will run it
				print self._get_time()+"Copying "+self.name()+".conf files into: C:\\beefs-tester\\superzz\\conf\\"+self.name()+".conf"
				self.copy_files(self.machine(), self.conf_place(), "C:\\beefs-tester\\superzz\\conf\\"+self.name()+".conf")
			else:
				# Copy the configuration file of component in remote machine that will run it
				print self._get_time()+"Copying honeycomb.conf files into: C:/beefs-tester/superzz/conf/\honeycomb.conf"
				self.copy_files(self.machine(), self.conf_place(), "C:/beefs-tester/superzz/conf/honeycomb.conf")
				# Copy the configuration file of component in remote machine that will run it
				print self._get_time()+"Copying honeybee.conf files into: tmp/superzz/conf/honeybee.conf"
				self.copy_files(self.machine(), self.conf2_place(), "C:\\beefs-tester\\superzz\\conf\\honeybee.conf")
			
		
			
		
			if self.name() is "honeycomb" or self.name() is "combee":
				print self._get_time()+"Making directories needed to run BeeFS..."
				self.execute("mkdir "+self.conf()["contributing_storage.directory"], self.machine())
			if self.name() is "honeybee" or self.name() is "combee":
				print self._get_time()+"Making directories needed to run BeeFS..."
				if self.name() is "combee":
					self.execute_on_windows("mkdir "+self.conf2()["mount_directory"], self.machine())
				else:
					self.execute_on_windows("mkdir "+self.conf()["mount_directory"], self.machine())
				# Copy workload zip
				print self._get_time()+"Copying workload.zip into C:\\beefs-tester\\"
				self.copy_workload( self.machine(), workload_path)

		
		
	def unmount(self):
		# removing the directory that contains BeeFS main files
		print self._get_time()+"Removing the BeeFS main directory..."
		self.execute("rm -r /tmp/superzz", self.machine())
		self.execute("rm -r /tmp/workloadzz", self.machine())
		self.clear()

	def identify_SO(self): #this method must be *runned* before all others
		self.__so = self.execute("python -m platform", self.machine())[0].split("-")[0]

	def kill_others(self, component):
			out, err, rcod = self.execute("ps xau | grep " + 
                              	   	component + 
                                 	 " | grep "+user+"| grep -v grep", self.machine())
			if "port 22: No route to host" in out:
				print self._get_time()+self.machine()+" doesn't respond"
				return False
      		        if out.split()!=[]:
				print self._get_time()+"There is another instance of "+self.name()+" running on "+self.machine()
				print self._get_time()+"Killing now... Process "+out.split()[1]
				self.execute("kill "+out.split()[1], self.machine())	
			return True
			


	def clear(self):
		# Cleaning metadata of component to start a new test
		if self.name() is "queenbee":
			print self._get_time()+"Removing Queenbee.d and others metadata files..."
			self.execute("rm "+self.conf()["metadata_directory"]+sep+"Queenbee.*", self.machine())
		if self.name() is "honeycomb" or self.name() is "combee":
			print self._get_time()+"Cleaning the storage and removing honeycomb metadata files..."
			self.execute("rm "+self.conf()["contributing_storage.directory"]+sep+"*", self.machine())
			self.execute("rm "+self.conf()["metadata_directory"]+sep+"Honeycomb.*", self.machine())
		print self._get_time()+"Cleaning previous files..."
		self.execute("rm -r /tmp/superzz", self.machine())
		self.execute("rm -r /tmp/super.zip", self.machine())
		self.execute("rm -r /tmp/workloadzz", self.machine())
		self.execute("rm -r /tmp/workload.zip", self.machine())
	
	def test(self, workload_path):
		# this script must be in beefs directory where exists \conf 
		print self._get_time()+'Starting the test...Copying files into mount point'
		if self.name() == "honeybee": 
			honeybee = self.conf()
			honeycomb = self.conf2()
		else:	
			honeybee = self.conf2()
			honeycomb = self.conf()
		if self.so() == "Linux":
			source = "/tmp/workloadzz"
			dest = honeybee['mount_directory']
			command = "cp -r "+source+"/ "+dest+"/workload/" #"cp -r /tmp/workloadzz/ /tmp/beefs-mount/"
		else: 
			source = "C:\\beefs-tester\\workloadzz"
			dest = 'Z:\ '
			command = 'copy "'+source+'\*.*" "'+dest+'\\"'
		queenbee = honeycomb['osdmaster'].split(':')
		
		psw = "09442518461j"#getpass.getpass("Password to "+user+"@"+machine())
		
		self.execute('ssh '+self.machine()+' "echo '+psw+' | sudo -S mkdir '+dest+'/workload/"', self.machine())
		self.execute('ssh '+self.machine()+' "echo '+psw+' | sudo -S chown joopeeds '+dest+'/workload"', self.machine())
		if queenbee[0]=="localhost":
			allocation = "local"
		else:
			allocation = "distributed"
		mode = honeycomb['file_synchronization'] +" , " + allocation + " and "+ self.name()
		hostname = self.machine()
		workload = workload_path.split(sep)[-1]
		self.execute("unzip -o "+workload+" -d workloadzz", None)
		size = getsize("workloadzz")
		self.execute("rm -r workloadzz/", None)
		dt = datetime.datetime.now()
		test = ' Test on '+ self.so() +' '+ dt.strftime("%d/%m/%Y %H:%M:%S")
		header = '#'*60 + '\n' + generateheader(test) + generateheader("Hostname of honeycomb: "+hostname) + generateheader("Queenbee on "+queenbee[0]) + generateheader("Mode: "+mode) + generateheader("Workload: "+ size)
		work = workload.split('.')[0]
		log = open('testlogs'+sep+work+sep+honeycomb['file_synchronization']+sep+allocation+sep+self.name()+sep+'test.log.'+dt.strftime("%d-%m-%Y.%Hh%Mmin%Ss")+'.log','w')
		log.write(header)	
		self.copy_files(self.machine(), 'copy.py', '/tmp/')
		time = self.execute('python /tmp/copy.py "'+command+'" ', self.machine())[0].split('\n')[0]
		body =  'Copying from '+source+' to '+dest +'\n' + 'Command executed: '+command + '\n' + 'elapsed: ' + time +'s\n' + '#'*60 + '\n'
		print self._get_time()+'Writting the log now...'
		log.write(body)
		log.close()
		print self._get_time()+'ending the test now...'
	

	


	def start(self, workload_path):
		def componentisrunning(self):
			sleep(5)
        		out, err, rcod = self.execute("ps xau | grep " + 
                              	   	self.name().capitalize() + 
                                 	 " | grep "+user+"| grep -v grep", self.machine())
      		        return out #if it is running, out is not empty, so it's is true
		def componentismounted(self):
			if self.name() == "honeybee": honeybee = self.conf()
			else:honeybee = self.conf2()
        		out, err, rcod = self.execute("df" + 
                                 	 " | grep "+honeybee['mount_directory']+"| grep -v grep", self.machine())
			return out #if it is running, out is not empty, so it's is true
		# try to start component and return whether it is running or not
		print self._get_time()+"Starting "+self.name()+" and waiting confirmation"
		if self.so()=="Linux":
			self.execute("bash /tmp/superzz/bin/beefs start "+self.name(), self.machine())
		else:
			self.start_on_windows("cd C:\\beefs-tester\\superzz\\", self.machine())
		if componentisrunning(self):
			print self._get_time()+self.name()+" is already running on "+self.machine()
			if self.name()=="honeybee" or self.name()== "combee": 
				if componentismounted(self):
					print self._get_time()+"Mount point mounted!"
					self.test(workload_path)
				else:
					print self._get_time()+"Mount point was not mounted, test couldn't be started"
				#pass
		else:
			print self._get_time()+self.name()+" was NOT started on "+self.machine()
			if self.name()=="honeybee" or self.name()== "combee": 
				print "Test couldn't be started"

	def stop(self):
		def componentisrunning(self):
			sleep(5)
        		out, err, rcod = self.execute("ps xau | grep " + 
                              	   	self.name().capitalize() + 
                                 	 " | grep "+user+"| grep -v grep", self.machine())
			return out
		# try to stop component and return whether it is running or not
		print self._get_time()+"Stopping "+self.name()+" and waiting confirmation"
		self.execute("bash /tmp/superzz/bin/beefs stop "+self.name(), self.machine())
		if not componentisrunning(self):
			print self._get_time()+"Ok, "+self.name()+" is not running anymore. Stopped"
		else:	print self._get_time()+self.name()+" was not stopped!"


def openconf(file):

	def fn(line):
 	   if line[0] == "#":
 	       line = ""
 	   else:
 	       idx = re.search (r"[^\\]#", line)
 	       if idx != None:
 	           line = line[:idx.start()+1]
 	   # Split non-comment into key and value.
 	   idx = re.search (r"=", line)
 	   if idx == None:
  	      key = line
  	      val = ""
 	   else:
  	      key = line[:idx.start()]
  	      val = line[idx.start()+1:]
  	   val = val.replace("\\#", "#")
  	   return (key.strip(),val.strip())

        config = {}
        new = open(file).read()
        for i in new.split('\n'):
                if fn(" "+i)[0]!='':
                        config[fn(" "+i)[0]] = fn(" "+i)[1]
        return config

def opencomponentconf(file):

	def fn(line):
   		  # Split line into non-comment and comment.
		 line = " " + line
   		 comment = ""
  		 if line[0] == "#":
  		      comment = line
  		      line = ""
  		 else:
 		      idx = re.search (r"[^\\]#", line)
 		      if idx != None:
 		           comment = line[idx.start()+1:]
 		           line = line[:idx.start()+1]

 		   # Split non-comment into key and value.

   		 idx = re.search (r"=", line)
   		 if idx == None:
   		     key = line
   		     val = ""
  		 else:
   		     key = line[:idx.start()]
   		     val = line[idx.start()+1:]
  		 val = val.replace ("\\#", "#")

  		 return (key.strip(),val.strip(),comment.strip())

        config = []
        new = open(file).read().split("[========]")
	zipped_path = new[0].split()[2].split('\n')[0]
	for i in range(len(new)):
		config.append({})
	for uni in range(1,len(new)):
        	for i in new[uni].split('\n'):
              	  if fn(i)[0]!='':
                        config[uni][fn(i)[0]] = fn(i)[1]
        return zipped_path, config[1:] # returns the zip path that was in header of .conf and a list of dicts containing info confs

def getsize(source):
	folder_size = 0
	num_files = 0
	for (path, dirs, files) in os.walk(source):
  		for file in files:
    			filename = os.path.join(path, file)
    			folder_size += os.path.getsize(filename)
			num_files += 1
	return "%.1fMB %d files" % (folder_size/(1024*1024.0), num_files)


def get_time():
		return int(datetime.datetime.now().strftime("%H")), int(datetime.datetime.now().strftime("%M"))

def generateheader(text):
	return  '#'*((60-len(text+'  '))/2) +' '+ text+' ' + '#'*((60-len(text+'  '))/2) +'\n'


def main(samples_config, zipped_path):
	for sample_config in samples_config:
	    	while True: 
			if get_time()[0] not in range(0,5)+range(18,24): break
		sys.stdout.flush()
		if sample_config != {}:
			if not sample_config.has_key("combee"):
		 	 samples = sample_config['samples']
		 	 queenbee = sample_config['queenbee']
		 	 queenbee_conf = sample_config['queenbee_conf']
		 	 honeycomb = sample_config['honeycomb']
		 	 honeycomb_conf = sample_config['honeycomb_conf']
		 	 honeybee = sample_config['honeybee']
		 	 honeybee_conf = sample_config['honeybee_conf']
		 	 files_to_write = sample_config['files_to_write']
		 	 data_server = Component("honeycomb", honeycomb, honeycomb_conf, "", zipped_path)
		 	 meta_server = Component("queenbee", queenbee, queenbee_conf, "", zipped_path)
		 	 client = Component("honeybee", honeybee, honeybee_conf, honeycomb_conf, zipped_path)
			 for i in range(int(sample_config['samples'])):
				#print sample_config['files_to_write']
				meta_server.clear()
				data_server.clear()
				client.clear()
				if not meta_server.kill_others("Queenbee"): continue
				if not data_server.kill_others("Combee"): continue
				if not data_server.kill_others("Honeycomb"): continue
				if not client.kill_others("Honeybee"): continue
				meta_server.mount(sample_config['files_to_write'])
				data_server.mount(sample_config['files_to_write'])
				client.mount(sample_config['files_to_write'])
				#sleep(180)
				meta_server.start(sample_config['files_to_write'])
				data_server.start(sample_config['files_to_write'])
				client.start(sample_config['files_to_write'])
				sys.stdout.flush()
				#sleep(180)
				client.stop()
				data_server.stop()
				meta_server.stop()
				data_server.unmount()
				meta_server.unmount()
				client.unmount()
			else:
			 samples = sample_config['samples']
		 	 queenbee = sample_config['queenbee']
		 	 queenbee_conf = sample_config['queenbee_conf']
		 	 combee = sample_config['combee']
		 	 honeycomb_conf = sample_config['honeycomb_conf']
		 	 honeybee_conf = sample_config['honeybee_conf']
		 	 files_to_write = sample_config['files_to_write']
		 	 combee = Component("combee", combee, honeycomb_conf, honeybee_conf, zipped_path)
		 	 meta_server = Component("queenbee", queenbee, queenbee_conf, "", zipped_path)
			 for i in range(int(sample_config['samples'])):
				print sample_config['files_to_write']
				meta_server.clear()
				combee.clear()
				if not meta_server.kill_others("Queenbee"): continue
				if not combee.kill_others("Combee"): continue
				if not combee.kill_others("Honeycomb"): continue
				if not combee.kill_others("Honeybee"): continue	
				meta_server.mount(sample_config['files_to_write'])
				combee.mount(sample_config['files_to_write'])
				#sleep(180)
				meta_server.start(sample_config['files_to_write'])
				combee.start(sample_config['files_to_write'])
				sys.stdout.flush()
				#sleep(180)
				combee.stop()
				meta_server.stop()
				meta_server.unmount()
				combee.unmount()


if __name__ == "__main__":

	if len(sys.argv) != 2:
	   
       	   sys.stderr.write("Usage: python beefstester.py config_file\n")
           sys.exit(-1)

	config_file = sys.argv[1]
	#FIXME
	zipped_path, samples_config = opencomponentconf(config_file)
	#FIXME
	main(samples_config, zipped_path)




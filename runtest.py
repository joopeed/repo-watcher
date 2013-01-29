#!/usr/bin/python
# coding: utf-8

import popen2, subprocess, socket, os, sys, re, platform, datetime, time


so = platform.system()
if so == "Linux":
	sep = '/'
else:
	sep = '\\'
user = "joopeeds"

class Component:
	def __init__(self, name, machine, conf, zipped_path):
        	self.__name = name
		self.__machine = machine
		self.__confplace = conf
		self.__conf = openconf(conf)
		self.__zipped_path = zipped_path 


	def name(self):
        	return self.__name
	
	def conf(self):
        	return self.__conf

	def conf_place(self):
		return self.__confplace

	def machine(self):
        	return self.__machine

	def zipped(self):
        	return self.__zipped_path.split(" ")[-1][:-2]
	
	

	def execute(self, remote_command, machine_addr, delay=None):
    		process = subprocess.Popen(" ".join(["ssh",
	                                 user +"@" + machine_addr,
                                         remote_command]),
					 shell=True,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT)
   		out, err = process.communicate()
    		return out, err, process.returncode

	def copy_zip(self, machine, zipped_path):
		# Copy the zip from the path given in test_config.conf
        	remote_path = user+"@" + machine + ":/tmp/"
        	getdata_cmd = " ".join(["scp", "-r",
        	                        zipped_path,
        	                        remote_path])
        	process = subprocess.Popen(getdata_cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        	out, err = process.communicate()
        	return out, err, process.returncode

	def copy_workload(self,  machine, workload_path):
		# Copy the zip from the path given in test_config.conf
        	remote_path = user+"@" + machine + ":/tmp/"
        	getdata_cmd = " ".join(["scp", "-r",
        	                        workload_path,
        	                        remote_path])
		workload = workload_path.split(sep)[-1]
        	process = subprocess.Popen(getdata_cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        	out, err = process.communicate()
        	return out, err, process.returncode

	def copy_files(self,  machine, src_path, dest_path):
		# Copy files from a path in this computer to a remote destination
        	remote_path = user+"@" + machine + ":/"+dest_path
        	getdata_cmd = " ".join(["scp", "-r",
        	                        src_path,
        	                        remote_path])
        	process = subprocess.Popen(getdata_cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        	out, err = process.communicate()
        	return out, err, process.returncode

    	def mount(self, workload_path):


		self.execute("rm -r /tmp/superzz", self.machine())
		self.execute("rm -r /tmp/"+self.zipped(), self.machine())
		self.execute("rm -r /tmp/workloadzz", self.machine())
		self.execute("rm -r /tmp/"+workload_path.split(sep)[-1], self.machine())
		# Copy BeeFS zip
		print "mounting beefs files on "+ self.machine()
		self.copy_zip(self.machine(), self.zipped())
		print "copying "+self.zipped()
		# Unzip the files of BeeFS
		print "unzipping beefs zip: "+ "unzip /tmp/"+self.zipped()+" -d /tmp/superzz"
		self.execute("unzip /tmp/"+self.zipped()+" -d /tmp/superzz", self.machine())
		# Remove the zip, already unzipped
		print "Removing zip..."
		self.execute("rm /tmp/"+self.zipped(), self.machine())

		# Copy the configuration file of component in remote machine that will run it
		print "Copying .conf files, probably: in "+"tmp/superzz/conf/"+self.name()+".conf"
		self.copy_files(self.machine(), self.conf_place(), "tmp/"+self.zipped()+"/conf/"+self.name()+".conf")
		
		if self.name() is "honeycomb":
			self.execute("mkdir "+self.conf()["contributing_storage.directory"], self.machine())
		elif self.name() is "honeybee":
			self.execute("mkdir "+self.conf()["mount_directory"], self.machine())
			# Copy workload zip
			self.copy_workload( self.machine(), workload_path)
			# Unzip the files of workload FIXME
			workload = workload_path.split(sep)[-1]
			print "unzipping workload: "+"unzip /tmp/"+workload+" -d /tmp/workloadzz"
			self.execute("unzip /tmp/"+workload+" -d /tmp/workloadzz", self.machine())
			# Remove the zip, already unzipped
			#self.execute("rm /tmp/"+workload, self.machine())
		
		
	def unmount(self):
		# removing the directory that contains BeeFS main files
		self.execute("rm -r /tmp/"+self.zipped(), self.machine())
		self.clear()

	def clear(self):
		# Cleaning metadata of component to start a new test
		if self.name is "queenbee":
			execute("rm "+conf["metadata_directory"]+sep+"Queenbee.*", machine())
		if self.name is "honeycomb":
			execute("rm "+conf["contributing_storage.directory"]+sep+"*", machine())
			execute("rm "+conf["metadata_directory"]+sep+"Honeycomb.*", machine())
		
	
	def start(self):
		def componentisrunning(self):
        		out, err, rcod = self.execute("ps xau | grep " + 
                              	   	self.name() + 
                                 	 " | grep -v grep", self.machine())
			print out
      		        return out #if it is running, out is not empty, so it's is true

		# try to start component and return whether it is running or not
		print "Now: "+"bash /tmp/superzz/bin/beefs start "+self.name()
		self.execute("bash /tmp/superzz/bin/beefs start "+self.name(), self.machine())
		print "started"
		return componentisrunning(self)

	def stop(self):
		def componentisrunning(self):
        		out, err, rcod = self.execute("ps xau | grep " + 
                              	   	self.name() + 
                                 	 " | grep -v grep", self.machine())
      		        return out #if it is running, out is not empty, so it's is true

		# try to stop component and return whether it is running or not
		self.execute("bash /tmp/"+self.zipped()+"/bin/beefs stop "+self.name(), self.machine())
		return componentisrunning(self)

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
	zipped_path = new[0]
	for i in range(len(new)):
		config.append({})
	for uni in range(1,len(new)):
        	for i in new[uni].split('\n'):
              	  if fn(i)[0]!='':
                        config[uni][fn(i)[0]] = fn(i)[1]
	print config
        return zipped_path, config[1:] # returns the zip path that was in header of .conf and a list of dicts containing info confs

def getsize(source):
	folder_size = 0
	for (path, dirs, files) in os.walk(source):
  		for file in files:
    			filename = os.path.join(path, file)
    			folder_size += os.path.getsize(filename)
	return "%.1fMB" % (folder_size/(1024*1024.0))


def generateheader(text):
	return  '#'*((60-len(text+'  '))/2) +' '+ text+' ' + '#'*((60-len(text+'  '))/2) +'\n'


def main(samples_config, zipped_path):
	print len(samples_config)
	for sample_config in samples_config:
		 if sample_config != {}:
		 	samples = sample_config['samples']
		 	queenbee = sample_config['queenbee']
		 	queenbee_conf = sample_config['queenbee_conf']
		 	honeycomb = sample_config['honeycomb']
		 	honeycomb_conf = sample_config['honeycomb_conf']
		 	honeybee = sample_config['honeybee']
		 	honeybee_conf = sample_config['honeybee_conf']
		 	files_to_write = sample_config['files_to_write']
		 	data_server = Component("honeycomb", honeycomb, honeycomb_conf, zipped_path)
		 	meta_server = Component("queenbee", queenbee, queenbee_conf, zipped_path)
		 	client = Component("honeybee", honeybee, honeybee_conf, zipped_path)

			 for i in range(int(sample_config['samples'])):
				print sample_config['files_to_write']
				data_server.mount(sample_config['files_to_write'])
				meta_server.mount(sample_config['files_to_write'])
				#client.mount(sample_config['files_to_write'])
				#data_server.clear()
				#meta_server.clear()
				data_server.start()
				meta_server.start()
				client.start()
				#data_server.stop()
				#meta_server.stop()
				#client.stop()
				#data_server.unmount()
				#meta_server.unmount()
				#client.unmount()



	"""
	# this script must be in beefs directory where exists \conf  
	honeybee = openconf('conf'+sep+'honeybee.conf')
	honeycomb = openconf('conf'+sep+'honeycomb.conf')
	source = sys.argv[1] # Type the origem without the last '\'
	if so == "Linux":
		dest = honeybee['mount_directory']
		command = 'cp -r '+source+'/ '+dest+'/\n'
	else: 
		command = 'copy "'+source+'\*.*" "'+dest+'\\" \n'

	queenbee = honeycomb['osdmaster'].split(':')
	if queenbee[0]=="localhost":
		allocation = "Non-Distributed"
	else:
		allocation = "Distributed"
	mode = honeycomb['file_synchronization'] + allocation
	hostname = socket.gethostname()
	size = getsize(source)
	queenbee = honeycomb['osdmaster'].split(':')

	dt = datetime.datetime.now()
	test = ' Test on '+ platform.system() +' '+ dt.strftime("%d/%m/%Y %H:%M ")
	header = '#'*60 + '\n' + generateheader(test) + generateheader("Hostname of honeycomb: "+hostname) + generateheader("Queenbee on "+queenbee[0]) + generateheader("Mode: "+mode) + generateheader("Workload: "+ size)
	log = open('testlogs'+sep+'test.log.'+dt.strftime("%d-%m-%Y.%Hh%M")+'.log','w')
	log.write(header)
	startepoch = int(time.time())
	popen2.popen2(command)[0].readlines()
	endepoch = int(time.time())
	body =  'Copying from '+source+' to '+dest +'\n' + 'Command executed: '+command + '\n' + 'elapsed: ' + str( endepoch - startepoch )  +'s\n' + '#'*60 + '\n'
	log.write(body)
	log.close()
	"""


if __name__ == "__main__":

	if len(sys.argv) != 2:
	   
       	   sys.stderr.write("Usage: python beefstester.py config_file\n")
           sys.exit(-1)

	config_file = sys.argv[1]
	#FIXME
	zipped_path, samples_config = opencomponentconf(config_file)
	#FIXME
	main(samples_config, zipped_path)




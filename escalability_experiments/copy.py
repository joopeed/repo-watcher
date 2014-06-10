import time, subprocess, sys, datetime
command = "cp -r /mnt/workload/* /mnt/beefs/test_place/place9" 
while True: 
	if datetime.datetime.now() >= datetime.datetime.strptime('12/8/2013 19:49', "%d/%m/%Y %H:%M"): break
startepoch = int(time.time())
process = subprocess.Popen(command,
			shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
out, err = process.communicate()
endepoch = int(time.time())
print datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
print endepoch - startepoch


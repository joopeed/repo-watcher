# You will need to config_vms if you are executing for the first time
# python config_vms.py
python clear_machines.py
python config_enviroment.py
for i in 1 2 3 4 5 6 7 8 9 10
do
	python start_beefs.py
	python set_copy_start.py
	sleep 300 #time to start collecting
	python collect_results.py $i
	python stop_beefs.py	
done
#python clear_machines.py

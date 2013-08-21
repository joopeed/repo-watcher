# coding: utf-8
import os

def get_results(source):
	results = {}
	folder_size = 0
	num_files = 0
	for (path, dirs, files) in os.walk(source):
  		for file in files:
    			filename = os.path.join(path, file)
			if not results.has_key(filename.split('/')[1]): results[filename.split('/')[1]] = {}
		for file in files:
    			filename = os.path.join(path, file)
			if not results[filename.split('/')[1]].has_key(filename.split('/')[2]): results[filename.split('/')[1]][filename.split('/')[2]] = {}
		for file in files:
    			filename = os.path.join(path, file)
			if not results[filename.split('/')[1]][filename.split('/')[2]].has_key(filename.split('/')[3]): results[filename.split('/')[1]][filename.split('/')[2]][filename.split('/')[3]] = {}
		for file in files:
    			filename = os.path.join(path, file)
			if not results[filename.split('/')[1]][filename.split('/')[2]][filename.split('/')[3]].has_key(filename.split('/')[4]): results[filename.split('/')[1]][filename.split('/')[2]][filename.split('/')[3]][filename.split('/')[4]] = [open(filename).read().split('\n')[8][9:-1]]
			else:
				results[filename.split('/')[1]][filename.split('/')[2]][filename.split('/')[3]][filename.split('/')[4]].append(open(filename).read().split('\n')[8][9:-1])
		
	return results
import math, time
print "\t".join(['Carga','Amostra', 'Decorrido', 'Sincronizacao','Distribuicao','Composicao'])
for workload, workload_values in get_results("testlogs/").items():
	for synchronization, synchronization_values in workload_values.items():
		for distribution, distribution_values in synchronization_values.items():
			for jvm, jvm_values in distribution_values.items():
				soma = 0
				for i in range(len(jvm_values)):
					soma+=float(jvm_values[i])
					#filo = open('results/'+key2+"_"+key3+"_"+key4+".txt",'a')
					#workload = workload.replace("workload", "Carga")
					#jvm = jvm.replace("honeybee", "JVMsDiferentes")
					#jvm = jvm.replace("combee", "MesmaJVM")
					#print "\t".join([workload, str(i+1), jvm_values[i],synchronization, distribution,jvm])
				media = soma/float(len(jvm_values))
				desvios = []
				devsqs = []
				for i in range(len(jvm_values)):
					desvios.append(float(jvm_values[i])-media)
					#print media, int(jvm_values[i])-media, jvm_values[i]
				
				avedev = sum(map(abs, desvios))/float(len(jvm_values))
				#print avedev
				#time.sleep(200)
				for i in range(len(jvm_values)):
					devsqs.append(desvios[i]*desvios[i])
				#time.sleep(200)
				desvio = math.sqrt(sum(map(float, devsqs))/len(jvm_values))
				print workload,synchronization, distribution, jvm, "Desvio", desvio,  "Media", media, "Quant", (100*1.96*desvio)/(5*media)
				
					

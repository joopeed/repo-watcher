beefs-tester
============

Beehive File System tester

Beehive File System ( lsd.ufcg.edu.br/beefs ) is a distributed file system for local area networks (LANs)
that is both scalable and simple to maintain. It is being developed at Distributed Systems Laboratory (LSD)
at Federal University of Campina Grande, Brazil.

This tester will analyze the behavior of BeeFS into different situations
(including changing the mode of file synchronization, workloads and so on),
will allow execute performance tests more mechanically and generate more results in less time

h2. Configuration file

Edit @test_config.conf@ and configuration of each test you want to do.
First of all set this path @zipped_path@:

<pre>
zipped_path = super.zip
[========]
samples = 2
queenbee = ourico
queenbee_conf = queenbee.conf
honeycomb = abelhinha
honeycomb_conf = honeycomb.conf
honeybee = abelhinha
honeybee_conf = honeybee.conf
files_to_write = workload.zip
</pre>

Below each @[=======]@ you have one test case configuration.
* Repeat this symbol more times if you want to do various experiments

h2. BeeFS zip and workloads

h3. zip the directory of BeeFS

<pre>zip beefs-trunk/ beefs.zip</pre>

h3. zip workloads

<pre>zip workload1/ workload1.zip</pre>


h2. Running


<pre>python beefs-tester.py config_file.conf</pre>

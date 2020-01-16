# trawsers - lightweight transactions benchmark

Trawsers implements lightweight transactions benchmark
on AWS EC2.

Trawsers has two major assets: configurations and actions.

A configuration defines a benchmarking profile: the number of
nodes, their hardware properties, the load profile (e.g.
read/write ratio) and so on. Configuraitons are editable by the
user and stored in conf/ directory.

Actions depend on the used configuration and implement
benchmarking steps: provisioning the nodes, starting/stopping
instsances, loading data and warming up, benchmarking, collecting
results and cleaning un/destroying instances.

After a single configuration is benchmarked, a report is collected
in report/ subdirectory with the same name as configuration name.

By default, trawsers runs all actions for all configurations.
Since some actions leave running AWS instances, one should always
end using trawsers with "trawsers distclean".

Please use

        $ ./trawsers.py --help

for a list of available individual actions.

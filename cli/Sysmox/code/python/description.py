description = '''Sysmox command-line interface for system monitoring.
This tool provides CPU and memory statistics with support for per-core output and interval-based measurements.

Main commands:

cpupercent or cpu%
Show CPU usage percentage.
Options:
-pc or --percore : show CPU usage per core
-i or --intervaltime : measure CPU usage over a given time interval (in seconds)

cpucount or cpu#
Show CPU core and thread information.
Options:
-c or --phycore : show number of physical CPU cores
-t or --thread : show number of CPU threads

cpu_time or cpuT
Show CPU time statistics.
Options:
-pc or --percore : show CPU time per core
-u or --user : show CPU time spent in user mode
-s or --system : show CPU time spent in system mode
-I or --idle : show CPU idle time

cpu_frequency or cpuF
Show CPU frequency information.
Options:
-pc or --percore : show frequency per core
-C or --current : show current CPU frequency
-m or --min : show minimum CPU frequency
-M or --max : show maximum CPU frequency
-i or --intervaltime : calculate min/max frequency over a time interval

mem#, totalmemory, totalmem, or mem total
Show total physical system memory.

mem avail, avalable memeory, or mem~
Show available system memory.

reconf or reconfig
Reconfigure Sysmox settings.

Global options:

-a or --all
Reserved for future global operations. This flag currently has no effect.'''
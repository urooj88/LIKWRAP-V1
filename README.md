# LIKWRAP-V1

LIKWRAP:	Measure the total energyconsumption of data parallel kernel while running on the HPC platform and also calulate the Dynamic energy of th parallel kernel using the RAPL interface on Intel CPUs and DRAM. Unit is [Joule].


**Required Software:**

1.	Likwid perfctor.
2.	Python compiler.
3.	Linux OS(Ubuntu, Fedora, etc.)

**Help and Understang:**

Likwid is a simple to instal and use toolsuite of command-line applications and a library for performance-oriented programmers. For more details, there are some available links to get dived into it.

**YouTube Link:**
https://www.youtube.com/playlist?list=PLxVedhmuwLq2CqJpAABDMbZG8Whi7pKsk

**Likwid Performance Tool:**
https://hpc.fau.de/research/tools/likwid/

**Supported Architectures:**

1. Intel
2. AMD
3. ARM
4. IBM

**How To Use:**

python3 <scriptname> --app-type paralle

python3 run_measure_energy_pmxm_likwid.py --app-type parallel







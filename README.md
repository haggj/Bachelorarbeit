# Benchmarking SIDH Implementations

This repository contains code to benchmark currently available SIDH implementations:
- SIKE
    - Reference Implementation
    - Optimized Implementation
    - Optimized Implementation Compressed
    - x64 Implementation
    - x64 Implementation Compressed
- CIRCL
    - x64 Implementation
    - Generic Implementation
- Microsoft
    - Generic Implementation
    - Generic Implementation Compressed
    - x64 Implementation
    - x64 Implementation Compressed
- ECDH (used for comparison)
# Usage

1. Make sure you have installed ```docker``` on your system.
2. Checkout this repository.
3. The following commands are available by running the script ```run.sh```:
    - ```./run.sh build```<br>
      This command builds the docker container with all needed dependencies.
    - ```./run.sh benchmark```<br>
      This command builds and runs the benchmarking suite. The generated data by the benchmarking suite will be available in new ```data/``` subfolder in your current directory (for details see secion output files below).
    - ```./run.sh test```<br>
      This command executes unittests of the benchmarking suite.
    - ```./run.sh coverage```<br>
      This command executes unittests and list the coverage of the tests.
    - ```./run.sh bash```<br>
      Opens a interactive terminal within the docker container
4. Analyse output files in ```data/```.

# Output files
The following output files are generated:

- ```data/result.html```: Contains an overview about all measured benchmarks. All values are absolute instruction counts, except the memory column, which contains the maximum of used memory in bytes during execution.

- ```data/<curve>_mem.png```: Bar chart showing the maximum memory usage of each implementation initialized with \<curve\>.

- ```data/<curve>.png```: Bar chart showing the absolute instruction counts for each implementation initialized with \<curve\>.

- ```data/cached.json```: Contains cached JSON Data, that can be read by the application to produce the output graphs and html. The idea is to save the internal status for later use. The benchmarking application checks if the file "cached.json" exists in it's local directory. If the file is found, the cached data is used and benchmarking takes less time. If you want to use cached data within the docker container, simply copy that file to .cached/cached.json.

# SIDH Security Levels
The assumed security levels of the SIDH parameters, as described by [NIST](https://csrc.nist.gov/CSRC/media/Projects/Post-Quantum-Cryptography/documents/call-for-proposals-final-dec-2016.pdf) and [SIKE](https://sike.org/files/SIDH-spec.pdf):

	p434: 128-AES
	p503: 256-SHA
	p610: 192-AES
	p751: 256-AES

**NOTE:** Each output file contains ECDH benchmarks as reference value. The following elliptic curves are used to match the appropriate security classes:

    p434 and secp256r1 matching 128-Bit AES security
    p610 and secp384r1 matching 192-Bit AES security
    p751 and secp521r1 matching 256-Bit AES security
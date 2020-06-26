# Benchmarking SIDH Implementations

This repository contains code to benchmark currently available SIDH implementations:
- SIKE
    - Reference Implementation
    - Optimized Implementation
    - Optimized Implementation Compressed
    - x64 Implementation
    - x64 Implementation Compressed
- CIRCL
- Microsoft (tbd)

# Usage

1. Make sure you have installed ```docker``` on your system.
1. Checkout this repository.
2. Run the script ```./run.sh```. This will:
    - build the docker container specified in the Dockerfile
    - run all benchmarks within that docker environment
    - extract diagrams and a html overview into a subfolder ```data/``` within your current directory
3. Analyse output files in ```data/```.

# Output files
The following output files are generated:

- ```data/result.html```: Contains an overview about all measured benchmarks. All values are absolute instruction counts, except the memory column, which contains the maximum of used memory in bytes during execution.

- ```data/<curve>_mem.png```: Bar chart showing the maximum memory usage of each implementation initialized with \<curve\>.

- ```data/<curve>.png```: Bar chart showing the absolute instruction counts for each implementation initialized with \<curve\>.

**NOTE:** SIKE Reference Implementation is very slow and makes bar charts hard to read. Therefor, that implementation will not be listed in the charts. However, the benchmarks are executed and results can be seen in ```data/results.html```

**NOTE:** Each output file contains ECDH (via Curve25519) benchmarks as reference value.

# SIDH Security Level
The assumed security levels of the SIDH parameters, as described by [NIST](https://csrc.nist.gov/CSRC/media/Projects/Post-Quantum-Cryptography/documents/call-for-proposals-final-dec-2016.pdf) and [SIKE](https://sike.org/files/SIDH-spec.pdf):

	p434: 128-AES
	p503: 256-SHA
	p610: 192-AES
	p751: 256-AES

    As reference, ECDH:
	CURVE25519: 128-AES

#include <x86intrin.h>

unsigned long long int cpu_cycles(void);

//Resulting form INTEL paper
unsigned long benchmark_start(void);
unsigned long benchmark_stop(void);

unsigned int cycles_to_ms(unsigned long cycles);
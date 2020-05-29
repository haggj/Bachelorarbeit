#include <countcpu.h>

unsigned long long int cpu_cycles(void){
    return  __rdtsc();
}



unsigned long benchmark_start(void) { 
    unsigned int cycles_high, cycles_low;
    
    asm volatile    ("CPUID\n\t"           
                    "RDTSC\n\t"           
                    "mov %%edx, %0\n\t"           
                    "mov %%eax, %1\n\t": "=r" (cycles_high), "=r" (cycles_low)::"%rax", "%rbx", "%rcx", "%rdx"); 

    unsigned long r = ((unsigned long) cycles_high << 32) |  ((unsigned long) cycles_low);
    return r;
}

unsigned long benchmark_stop(void){
    unsigned int cycles_high, cycles_low;
    asm   volatile  ("RDTSCP\n\t"          
                    "mov %%edx, %0\n\t"          
                    "mov %%eax, %1\n\t"    
                    "CPUID\n\t": "=r" (cycles_high), "=r" (cycles_low):: "%rax", "%rbx", "%rcx", "%rdx");
    
    unsigned long r = ((unsigned long) cycles_high << 32) |  ((unsigned long) cycles_low);
    return r;
}


unsigned int cycles_to_ms(unsigned long cycles){
    //2,3 GHZ Processor
    return (unsigned int) (cycles+1500000)/2300000;
}
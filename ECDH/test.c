#include <stdio.h>
#include <stdlib.h>

#include <openssl/evp.h>
#include <openssl/ec.h>

#include <countcpu.h>

#define REPETITIONS 500

typedef unsigned long CYCLES;


void handleErrors(){
    printf("Error");
    exit(0);
}

void benchmark_keygen(const int rep)
{
	EC_KEY *key;
	if(NULL == (key = EC_KEY_new_by_curve_name(NID_X9_62_prime256v1))) handleErrors();

	unsigned long long int sum = 0;
	for(int i = 0; i < rep; i++){
		
		CYCLES start = benchmark_start();
		EC_KEY_generate_key(key);
		CYCLES stop = benchmark_stop();
		sum += stop - start;
	}  
  printf("Average: %li\t", (unsigned long) (sum/rep));

}


void main(){
    benchmark_keygen(REPETITIONS);
}
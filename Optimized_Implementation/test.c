#include <stdio.h>
#include <stdlib.h>

#include <countcpu.h>


#include <api.h>

#include <openssl/dh.h>
#include <openssl/ecdh.h>



#define REPETITIONS 5

typedef unsigned long CYCLES;


int benchmark_keygen(const int rep) {

  unsigned char private_key[SIDH_SECRETKEYBYTES] = { 0 };
  unsigned char public_key[SIDH_PUBLICKEYBYTES] = { 0 };

  unsigned long long int sum = 0;
  for(int i = 0; i < rep; i++){
      CYCLES start = benchmark_start();
      random_mod_order_A(private_key);
      EphemeralKeyGeneration_A(private_key, public_key);
      CYCLES stop = benchmark_stop();
      sum += stop - start;
  }  
  printf("Average: %li\t", (unsigned long) (sum/rep));


}


int main() {

  benchmark_keygen(REPETITIONS);
  return 0;


}
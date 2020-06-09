#include <stdio.h>
#include <stdlib.h>


#include <api.h>

#include <openssl/dh.h>
#include <openssl/ecdh.h>



#define REPETITIONS 1

typedef unsigned long CYCLES;


int benchmark_keygen(const int rep) {

  unsigned char private_key_A[SIDH_SECRETKEYBYTES] = { 0 };
  unsigned char public_key_A[SIDH_PUBLICKEYBYTES] = { 0 };

  unsigned char private_key_B[SIDH_SECRETKEYBYTES] = { 0 };
  unsigned char public_key_B[SIDH_PUBLICKEYBYTES] = { 0 };

  unsigned char shared_secret[SIDH_BYTES] = { 0 };


  random_mod_order_A(private_key_A);
  random_mod_order_B(private_key_B);

#ifdef COMPRESSED
      EphemeralKeyGeneration_Compressed_A(private_key_A, public_key_A); 
      EphemeralKeyGeneration_Compressed_B(private_key_B, public_key_B);
      
      EphemeralSecretAgreement_Compressed_A(private_key_A, public_key_B, shared_secret);
      EphemeralSecretAgreement_Compressed_B(private_key_A, public_key_B, shared_secret);
        
#else
      EphemeralKeyGeneration_A(private_key_A, public_key_A); 
      EphemeralKeyGeneration_B(private_key_B, public_key_B);
      
      EphemeralSecretAgreement_A(private_key_A, public_key_B, shared_secret);
      EphemeralSecretAgreement_B(private_key_A, public_key_B, shared_secret);
#endif


}


int main() {

  benchmark_keygen(REPETITIONS);
  return 0;


}
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#if PARAM==434
  #include <p434.c>
#elif PARAM==503
 #include <p503.c>
#elif PARAM==610
  #include <p610.c>
#elif PARAM==751
  #include <p751.c>
#endif

int __attribute__ ((noinline)) benchmark_keygen() {

  unsigned char PrivateKeyA[SIDH_SECRETKEYBYTES_A], PrivateKeyB[SIDH_SECRETKEYBYTES_B];
  unsigned char PublicKeyA[SIDH_PUBLICKEYBYTES], PublicKeyB[SIDH_PUBLICKEYBYTES];
  unsigned char SharedSecretA[SIDH_BYTES], SharedSecretB[SIDH_BYTES];

  random_mod_order_A(PrivateKeyA);
  random_mod_order_B(PrivateKeyB);

  EphemeralKeyGeneration_A(PrivateKeyA, PublicKeyA);                            // Get some value as Alice's secret key and compute Alice's public key
  EphemeralKeyGeneration_B(PrivateKeyB, PublicKeyB);                            // Get some value as Bob's secret key and compute Bob's public key
  EphemeralSecretAgreement_A(PrivateKeyA, PublicKeyB, SharedSecretA);           // Alice computes her shared secret using Bob's public key
  EphemeralSecretAgreement_B(PrivateKeyB, PublicKeyA, SharedSecretB);           // Bob computes his shared secret using Alice's public key

  if (memcmp(SharedSecretA, SharedSecretB, SIDH_BYTES) != 0) {
     printf("Not Equal!!!");
  }
}


int main() {

  benchmark_keygen();
  return 0;


}
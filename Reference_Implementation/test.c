#include <stdio.h>
#include <sidh.h>
#include <time.h>
#include <stdlib.h>

#include <test_sike.h>
#include <sike_params.h>
#include <countcpu.h>

#include <sidh.h>
#include <unistd.h>

#define REPETITIONS 1

typedef unsigned long CYCLES;

int benchmark_keygen(const int rep) {

  //Define Parameters
  const sike_params_raw_t *params_raw = &SIKEp434;
  sike_params_t params = { 0 };
  sike_setup_params(params_raw, &params);
  ff_Params* pA = params.EA.ffData;
  ff_Params* pB = params.EB.ffData;
  
  //Private Keys init
  mp privateKey_A, privateKey_B;
  pA->init(pA, privateKey_A);
  pB->init(pB, privateKey_B);

  //Pulbic Keys Init
  sike_public_key_t publicKey_A = { 0 }, publicKey_B = { 0 };
  public_key_init(pA, &publicKey_A);
  public_key_init(pB, &publicKey_B); 

  //ALICE
  sidh_sk_keygen(&params, ALICE, privateKey_A);
  sidh_isogen(&params, &publicKey_A,privateKey_A, ALICE);

  //BOB
  sidh_sk_keygen(&params, BOB, privateKey_B);
  sidh_isogen(&params, &publicKey_B,privateKey_B, BOB);

}


int main() {

  benchmark_keygen(REPETITIONS);
  return 0;


}
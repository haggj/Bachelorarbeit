#include <stdio.h>
#include <sidh.h>
#include <time.h>
#include <stdlib.h>

#include <test_sike.h>
#include <sike_params.h>

#include <sidh.h>
#include <unistd.h>


int benchmark_keygen_A(sike_params_t params, sike_public_key_t publicKey_A, mp *privateKey_A) {

  ff_Params* pA = params.EA.ffData;
  
  //Pulbic Keys Init
  public_key_init(pA, &publicKey_A);
  //Private Keys init
  pA->init(pA, *privateKey_A);

  //ALICE
  sidh_sk_keygen(&params, ALICE, *privateKey_A);
  sidh_isogen(&params, &publicKey_A, *privateKey_A, ALICE);

}

int benchmark_keygen_B(sike_params_t params, sike_public_key_t publicKey_B, mp *privateKey_B) {

  ff_Params* pB = params.EB.ffData;
  
  //Public Key init
  public_key_init(pB, &publicKey_B); 

  //Private Key init
  pB->init(pB, *privateKey_B);

  //BOB
  sidh_sk_keygen(&params, BOB, *privateKey_B);
  sidh_isogen(&params, &publicKey_B, *privateKey_B, BOB);

}

int benchmark_secret_A(sike_params_t params, sike_public_key_t publicKey_B, mp privateKey_A){
  fp2 secret;
  fp2_Init(params.EA.ffData, &secret);
  sidh_isoex(&params, &publicKey_B, privateKey_A, ALICE, &secret);
}

int benchmark_secret_B(sike_params_t params, sike_public_key_t publicKey_A, mp privateKey_B){
  fp2 secret;
  fp2_Init(params.EB.ffData, &secret);
  sidh_isoex(&params, &publicKey_A, privateKey_B, BOB, &secret);

}

int main() {

//Define Parameters
#ifdef PARAM434
  const sike_params_raw_t *params_raw = &SIKEp434;  
#elif PARAM503
  const sike_params_raw_t *params_raw = &SIKEp503;
#elif PARAM610
  const sike_params_raw_t *params_raw = &SIKEp610;
#elif PARAM751
  const sike_params_raw_t *params_raw = &SIKEp751;
#endif

  sike_params_t params = { 0 };
  sike_setup_params(params_raw, &params);

  sike_public_key_t publicKey_A = { 0 };
  sike_public_key_t publicKey_B = { 0 };

  mp privateKey_A;
  mp privateKey_B;
  
  benchmark_keygen_A(params, publicKey_A, &privateKey_A);
  benchmark_keygen_B(params, publicKey_B, &privateKey_B);

  benchmark_secret_A(params, publicKey_B, privateKey_A);
  benchmark_secret_B(params, publicKey_A, privateKey_B);

}
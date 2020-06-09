#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include <openssl/evp.h>
#include <openssl/ec.h>


void benchmark_keygen()
{
	EVP_PKEY_CTX *pctx;
	EVP_PKEY_CTX *ctx;
	EVP_PKEY *key_A = NULL, *key_B = NULL;
	int status;

	/* Define Algorithm to be ED25519 */
	pctx = EVP_PKEY_CTX_new_id(EVP_PKEY_X25519, NULL);
	assert(pctx != NULL);

	/* Generate the keys */
	status = EVP_PKEY_keygen_init(pctx);
	assert(status == 1);
	status = EVP_PKEY_keygen(pctx, &key_A);
	assert(status == 1);
	status = EVP_PKEY_keygen(pctx, &key_B);
	assert(status == 1);


	/* Derivate secret*/
	unsigned char shard_secret;
	size_t size = 32;

	ctx = EVP_PKEY_CTX_new(key_A, NULL);
	assert(ctx != NULL);
	status = EVP_PKEY_derive_init(ctx);
	assert(status == 1);
  	status = EVP_PKEY_derive_set_peer(ctx, key_B);
  	assert(status == 1);
	
	status = EVP_PKEY_derive(ctx, &shard_secret, &size);
	assert(status == 1);
	assert(size == 32);
	
}



void main(){
    benchmark_keygen();
}
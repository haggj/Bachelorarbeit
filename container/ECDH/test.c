#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include <openssl/evp.h>
#include <openssl/ec.h>

int keygen_A(EVP_PKEY_CTX *ctx, EVP_PKEY **key_A){
	return EVP_PKEY_keygen(ctx, key_A);
}

int keygen_B(EVP_PKEY_CTX *ctx, EVP_PKEY **key_B){
	return EVP_PKEY_keygen(ctx, key_B);
}

int derive_A(EVP_PKEY_CTX *ctx, unsigned char *key, size_t *keylen){
	return EVP_PKEY_derive(ctx, key, keylen);
}

int derive_B(EVP_PKEY_CTX *ctx, unsigned char *key, size_t *keylen){
	return EVP_PKEY_derive(ctx, key, keylen);
}



void benchmark_keygen()
{
	EVP_PKEY_CTX *pctx;
	EVP_PKEY_CTX *ctx;
	EVP_PKEY *key_A = NULL, *key_B = NULL;
	int status;

	/* Define Algorithm to be Diffie-Hellman via Curve 25519 */
	pctx = EVP_PKEY_CTX_new_id(EVP_PKEY_X25519, NULL);
	assert(pctx != NULL);

	/* Generate the keys */
	status = EVP_PKEY_keygen_init(pctx);
	assert(status == 1);

	status = keygen_A(pctx, &key_A);
	assert(status==1);
	status = keygen_B(pctx, &key_B);
	assert (status==1);

	/* Derivate secret*/
	unsigned char shared_secret_A;
	unsigned char shared_secret_B;
	size_t size = 126;

	/* A */
	ctx = EVP_PKEY_CTX_new(key_A, NULL);
	assert(ctx != NULL);
	status = EVP_PKEY_derive_init(ctx);
	assert(status == 1);
  	status = EVP_PKEY_derive_set_peer(ctx, key_B);
  	assert(status == 1);
	status = derive_A(ctx, &shared_secret_A, &size);
	assert(status == 1);

	EVP_PKEY *key_A2 = NULL, *key_B2 = NULL;

	status = keygen_A(pctx, &key_A2);
	assert(status==1);
	status = keygen_B(pctx, &key_B2);
	assert (status==1);

	/* B */
	EVP_PKEY_CTX *ctx2;
	ctx2 = EVP_PKEY_CTX_new(key_B2, NULL);
	assert(ctx2 != NULL);
	status = EVP_PKEY_derive_init(ctx2);
	assert(status == 1);
  	status = EVP_PKEY_derive_set_peer(ctx2, key_A2);
  	assert(status == 1);
	status = derive_B(ctx2, &shared_secret_B, &size);
	assert(status == 1);

	//assert(shared_secret_A == shared_secret_B);
	
}



void main(){
    benchmark_keygen();
}
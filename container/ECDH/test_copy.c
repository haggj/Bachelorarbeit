#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include <openssl/evp.h>
#include <openssl/ec.h>
 #include <openssl/crypto.h>


void handleErrors(char* error){
	printf("Error: %s\n", error);
	assert(0);
}

int keygen_A(EC_KEY *key_A){
	if(1 != EC_KEY_generate_key(key_A)) 
		handleErrors("creating keys A");
}

int keygen_B(EC_KEY *key_B){
	if(1 != EC_KEY_generate_key(key_B)) 
		handleErrors("creating keys B");
}

int derive_A(char* secret_A, int secret_len, EC_KEY *key_A, EC_KEY *key_B){
	return ECDH_compute_key(secret_A, secret_len, EC_KEY_get0_public_key(key_B), key_A, NULL);
}

int derive_B(char* secret_B, int secret_len, EC_KEY *key_B, EC_KEY *key_A){
	return ECDH_compute_key(secret_B, secret_len, EC_KEY_get0_public_key(key_A), key_B, NULL);
}



void benchmark()
{
	#if PARAM==283
		int curve = NID_sect283r1;
	#elif PARAM==409
		int curve = NID_sect409r1;
	#elif PARAM==571
		int curve = NID_sect571r1;
	#endif
	EC_KEY *key_A, *key_B;
	int field_size, secret_len, ret;
	unsigned char *secret_A, *secret_B;

	/* Create an Elliptic Curve Key object and set it up to use the ANSI X9.62 Prime 256v1 curve */
	if(NULL == (key_A = EC_KEY_new_by_curve_name(curve))) handleErrors("creating key object A");
	if(NULL == (key_B = EC_KEY_new_by_curve_name(curve))) handleErrors("creating key object B");

	/* Generate the private and public key */
	keygen_A(key_A);
	keygen_B(key_B);

	/* Calculate the size of the buffer for the shared secret */
	field_size = EC_GROUP_get_degree(EC_KEY_get0_group(key_A));
	secret_len = (field_size+7)/8;

	/* Allocate the memory for the shared secret */
	if(NULL == (secret_A = OPENSSL_malloc(secret_len))) handleErrors("malloc secret");
	if(NULL == (secret_B = OPENSSL_malloc(secret_len))) handleErrors("malloc secret");

	/* Derive the shared secret */
	ret = derive_A(secret_A, secret_len, key_A, key_B);
	if(ret <= 0)
	{
		OPENSSL_free(secret_A);
		assert(0);
	}

	ret = derive_B(secret_B, secret_len, key_B, key_A);
	if(ret <= 0)
	{
		OPENSSL_free(secret_A);
		assert(0);
	}
	/* Clean up */
	EC_KEY_free(key_A);
	EC_KEY_free(key_B);

	assert(strcmp(secret_A, secret_B) == 0);	
	return;
	
}



void main(){
    benchmark();
}
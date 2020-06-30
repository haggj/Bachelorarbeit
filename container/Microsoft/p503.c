#ifdef COMPRESSED
    #include <P503_compressed_api.h> 
    #define random_mod_order_A            random_mod_order_A_SIDHp503
    #define random_mod_order_B            random_mod_order_B_SIDHp503
    #define EphemeralKeyGeneration_A      EphemeralKeyGeneration_A_SIDHp503_Compressed
    #define EphemeralKeyGeneration_B      EphemeralKeyGeneration_B_SIDHp503_Compressed
    #define EphemeralSecretAgreement_A    EphemeralSecretAgreement_A_SIDHp503_Compressed
    #define EphemeralSecretAgreement_B    EphemeralSecretAgreement_B_SIDHp503_Compressed
#else
    #include <P503_api.h>
    #define random_mod_order_A            random_mod_order_A_SIDHp503
    #define random_mod_order_B            random_mod_order_B_SIDHp503
    #define EphemeralKeyGeneration_A      EphemeralKeyGeneration_A_SIDHp503
    #define EphemeralKeyGeneration_B      EphemeralKeyGeneration_B_SIDHp503
    #define EphemeralSecretAgreement_A    EphemeralSecretAgreement_A_SIDHp503
    #define EphemeralSecretAgreement_B    EphemeralSecretAgreement_B_SIDHp503
#endif



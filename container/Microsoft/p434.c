#ifdef COMPRESSED
    #include <P434_compressed_api.h> 
    #define random_mod_order_A            random_mod_order_A_SIDHp434
    #define random_mod_order_B            random_mod_order_B_SIDHp434
    #define EphemeralKeyGeneration_A      EphemeralKeyGeneration_A_SIDHp434_Compressed
    #define EphemeralKeyGeneration_B      EphemeralKeyGeneration_B_SIDHp434_Compressed
    #define EphemeralSecretAgreement_A    EphemeralSecretAgreement_A_SIDHp434_Compressed
    #define EphemeralSecretAgreement_B    EphemeralSecretAgreement_B_SIDHp434_Compressed
#else
    #include <P434_api.h>
    #define random_mod_order_A            random_mod_order_A_SIDHp434
    #define random_mod_order_B            random_mod_order_B_SIDHp434
    #define EphemeralKeyGeneration_A      EphemeralKeyGeneration_A_SIDHp434
    #define EphemeralKeyGeneration_B      EphemeralKeyGeneration_B_SIDHp434
    #define EphemeralSecretAgreement_A    EphemeralSecretAgreement_A_SIDHp434
    #define EphemeralSecretAgreement_B    EphemeralSecretAgreement_B_SIDHp434
#endif



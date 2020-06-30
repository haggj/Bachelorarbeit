#ifdef COMPRESSED
    #include <P751_compressed_api.h> 
    #define random_mod_order_A            random_mod_order_A_SIDHp751
    #define random_mod_order_B            random_mod_order_B_SIDHp751
    #define EphemeralKeyGeneration_A      EphemeralKeyGeneration_A_SIDHp751_Compressed
    #define EphemeralKeyGeneration_B      EphemeralKeyGeneration_B_SIDHp751_Compressed
    #define EphemeralSecretAgreement_A    EphemeralSecretAgreement_A_SIDHp751_Compressed
    #define EphemeralSecretAgreement_B    EphemeralSecretAgreement_B_SIDHp751_Compressed
#else
    #include <P751_api.h>
    #define random_mod_order_A            random_mod_order_A_SIDHp751
    #define random_mod_order_B            random_mod_order_B_SIDHp751
    #define EphemeralKeyGeneration_A      EphemeralKeyGeneration_A_SIDHp751
    #define EphemeralKeyGeneration_B      EphemeralKeyGeneration_B_SIDHp751
    #define EphemeralSecretAgreement_A    EphemeralSecretAgreement_A_SIDHp751
    #define EphemeralSecretAgreement_B    EphemeralSecretAgreement_B_SIDHp751
#endif



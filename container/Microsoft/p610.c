#ifdef COMPRESSED
    #include <P610_compressed_api.h> 
    #define random_mod_order_A            random_mod_order_A_SIDHp610
    #define random_mod_order_B            random_mod_order_B_SIDHp610
    #define EphemeralKeyGeneration_A      EphemeralKeyGeneration_A_SIDHp610_Compressed
    #define EphemeralKeyGeneration_B      EphemeralKeyGeneration_B_SIDHp610_Compressed
    #define EphemeralSecretAgreement_A    EphemeralSecretAgreement_A_SIDHp610_Compressed
    #define EphemeralSecretAgreement_B    EphemeralSecretAgreement_B_SIDHp610_Compressed
#else
    #include <P610_api.h>
    #define random_mod_order_A            random_mod_order_A_SIDHp610
    #define random_mod_order_B            random_mod_order_B_SIDHp610
    #define EphemeralKeyGeneration_A      EphemeralKeyGeneration_A_SIDHp610
    #define EphemeralKeyGeneration_B      EphemeralKeyGeneration_B_SIDHp610
    #define EphemeralSecretAgreement_A    EphemeralSecretAgreement_A_SIDHp610
    #define EphemeralSecretAgreement_B    EphemeralSecretAgreement_B_SIDHp610
#endif



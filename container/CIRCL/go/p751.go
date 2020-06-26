// +build p751

package main

import (
	"github.com/cloudflare/circl/dh/sidh"
)

//export KeysInit
func KeysInit() {
	prvA = sidh.NewPrivateKey(sidh.Fp751, sidh.KeyVariantSidhA)
	prvB = sidh.NewPrivateKey(sidh.Fp751, sidh.KeyVariantSidhB)

	pubA = sidh.NewPublicKey(sidh.Fp751, sidh.KeyVariantSidhA)
	pubB = sidh.NewPublicKey(sidh.Fp751, sidh.KeyVariantSidhB)
}

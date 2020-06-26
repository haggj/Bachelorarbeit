// +build p503

package main

import (
	"github.com/cloudflare/circl/dh/sidh"
)

//export KeysInit
func KeysInit() {
	prvA = sidh.NewPrivateKey(sidh.Fp503, sidh.KeyVariantSidhA)
	prvB = sidh.NewPrivateKey(sidh.Fp503, sidh.KeyVariantSidhB)

	pubA = sidh.NewPublicKey(sidh.Fp503, sidh.KeyVariantSidhA)
	pubB = sidh.NewPublicKey(sidh.Fp503, sidh.KeyVariantSidhB)
}

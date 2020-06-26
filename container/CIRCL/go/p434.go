// +build p434

package main

import (
	"github.com/cloudflare/circl/dh/sidh"
)

func KeysInit() {
	prvA = sidh.NewPrivateKey(sidh.Fp434, sidh.KeyVariantSidhA)
	prvB = sidh.NewPrivateKey(sidh.Fp434, sidh.KeyVariantSidhB)

	pubA = sidh.NewPublicKey(sidh.Fp434, sidh.KeyVariantSidhA)
	pubB = sidh.NewPublicKey(sidh.Fp434, sidh.KeyVariantSidhB)
}

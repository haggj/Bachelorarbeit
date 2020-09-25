package main

import (
	"C"
	"crypto/rand"

	"github.com/cloudflare/circl/dh/sidh"
)

var prvA *sidh.PrivateKey
var prvB *sidh.PrivateKey

var pubA *sidh.PublicKey
var pubB *sidh.PublicKey

func main() {
	KeysInit()
	privateKeyA()
	privateKeyB()
	publicKeyA()
	publicKeyB()
	sharedA()
	sharedB()
}

func privateKeyA() {
	prvA.Generate(rand.Reader)
}

func privateKeyB() {
	prvB.Generate(rand.Reader)
}

func publicKeyA() {
	prvA.GeneratePublicKey(pubA)
}

func publicKeyB() {
	prvB.GeneratePublicKey(pubB)
}

func sharedA() {
	ssA := make([]byte, prvA.SharedSecretSize())
	prvA.DeriveSecret(ssA[:], pubB)
}

func sharedB() {
	ssB := make([]byte, prvB.SharedSecretSize())
	prvB.DeriveSecret(ssB[:], pubA)
}

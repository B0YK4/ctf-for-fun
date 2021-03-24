import random
from Crypto.Cipher import AES
r = open("11.txt", "r") 

def aes_random_key():
	key=''
	for i in range(16):
		key+=chr(random.randint(32,137))
	return key

def xor_strings(xs, ys):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))

def aes_ecb_encrypt(plaintext,key):
	obj = AES.new(key, AES.MODE_ECB)
	return obj.encrypt(plaintext)


def detect_AES_ECB(data):
	chunks=[data[key:key+16] for key in range(0, len(data)-16,16 ) ]
	for i in range (len(chunks)):
		for j in range(i+1,len(chunks)):
			if (any(chunks[i][x:4+x]==chunks[j][x:4+x] for x in range(12))):
				print "ECB",chunks[i]
				return
	print "CBC"
def encryption_oracle(input):
	r1=random.randint(5,10)
	plaintext=input
	plaintext+=(16-(len(plaintext)%16))*(chr(16-(len(plaintext)%16)))
	r3=random.randint(1, 2)
	aes_ecb_encrypt(plaintext,aes_random_key())
	


def main():
    key="QWERTGHBJKDSERTY"
    unknowntext="Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
	data = r.read()
	encryption_oracle(data)

	r.close()

if __name__ == '__main__':
    main()
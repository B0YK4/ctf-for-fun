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

def aes_cbc_encrypt(plaintext,key,iv):
	chunks=[plaintext[k:k+len(key)] for k in range(0, len(plaintext)-len(key),len(key) ) ]
	ciphertext=xor_strings(iv,aes_ecb_encrypt(chunks[0],key))
	for i in range(1,len(chunks)):
		ciphertext+=xor_strings(ciphertext[-len(key):],aes_ecb_encrypt(chunks[i],key))
	return ciphertext

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
	ciphertext=''
	if (r3==1):
		print "1: ECB"
		ciphertext= aes_ecb_encrypt(plaintext,aes_random_key())
	else:
		print "2: CBC"
		ciphertext= aes_cbc_encrypt(plaintext,aes_random_key(),aes_random_key())
	detect_AES_ECB(ciphertext)


def main():
	data = r.read()
	encryption_oracle(data)

	r.close()

if __name__ == '__main__':
    main()
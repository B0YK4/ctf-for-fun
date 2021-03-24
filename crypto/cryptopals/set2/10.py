from Crypto.Cipher import AES
import base64

w = open("10out.txt", "w")
r = open("10.txt", "r")

def xor_strings(xs, ys):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))

def aes_ecb_decrypt(ciphertext,key):
	obj = AES.new(key, AES.MODE_ECB)
	return obj.decrypt(ciphertext)

def aes_cbc_decrypt(ciphertext,key):
	chunks=[ciphertext[k:k+len(key)] for k in range(0, len(ciphertext)-len(key),len(key) ) ]
	plaintext=aes_ecb_decrypt(chunks[0],key)
	for i in range(1,len(chunks)):
		plaintext+=xor_strings(chunks[i-1],aes_ecb_decrypt(chunks[i],key))
	return plaintext


def main():
	key="YELLOW SUBMARINE"
	data = r.read().decode('base64')
	
	w.write(aes_cbc_decrypt(data,key))

	r.close()
	w.close()



if __name__ == '__main__':
    main()
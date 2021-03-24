from Crypto.Cipher import AES
import base64

w = open("7out.txt", "w")
r = open("7.txt", "r")

def aes_ecb_encrypt(plaintext,key):
	obj = AES.new(key, AES.MODE_ECB)
	return obj.encrypt(plaintext)

def aes_ecb_decrypt(ciphertext,key):
	obj = AES.new(key, AES.MODE_ECB)
	return obj.decrypt(ciphertext)

def main():
	key="YELLOW SUBMARINE"
	data = r.read().decode('base64')
	
	w.write(aes_ecb_decrypt(data,key))

	r.close()
	w.close()



if __name__ == '__main__':
    main()
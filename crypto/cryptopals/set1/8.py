import base64
r = open("8.txt", "r")

def detect_AES(data):
	l=0
	for line in data:
		l+=1
		ciphertex=line.strip().decode("hex")
		chunks=[ciphertex[key:key+16] for key in range(0, len(ciphertex)-16,16 ) ]
		for i in range (len(chunks)):
			for j in range(i+1,len(chunks)):
				if chunks[i]==chunks[j]:
					print "found it in line: "+str(l)
					return  line

def main():
	print detect_AES(r)
	r.close()



if __name__ == '__main__':
    main()
import base64
w = open("6out.txt", "w")
r = open("6.txt", "r")

def xor_strings(s1, s2):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(s1, s2))

def hamming_distance(s1,s2):
	return "".join(format(ord(x) ^ ord(y),'b') for x, y in zip(s1, s2)).count('1')

def smallest_normalized_keysize(s):
	smallest=1111111111111
	keysize=0
	for i in range(2,40):
		distances=[]
		chunks=[s[key:key+i] for key in range(0, len(s)-i,i ) ]
		for n in range(len(chunks)):
			for j in range(n+1,len(chunks)):
			  	distances.append(hamming_distance(chunks[n],chunks[j]))
		
		x=sum(distances)/len(distances)
		x/=i
		if(x<smallest):
			smallest=x
			keysize=i
	smallest=1111111111111
	keysize=0
	for i in range(2,40):
		distances=[]
		chunks=[s[key:key+i] for key in range(0, len(s)-i,i ) ]
		for n in range(len(chunks)):
			for j in range(n+1,len(chunks)):
			  	distances.append(hamming_distance(chunks[n],chunks[j]))
		
		x=sum(distances)/len(distances)
		x/=i
		if(x<smallest):
			smallest=x
			keysize=i

	return keysize


def transposed_blocks(data,keysize):
	s_key_blocks=[ data[i:i+keysize] for i in range(0, len(data)-keysize,keysize ) ]
	transposed2=list(s_key_blocks[0])
	for i in range(1,len(s_key_blocks)-1):
		for j in range(len(s_key_blocks[0])):
			transposed2[j]+=s_key_blocks[i][j]
	return transposed2


def get_the_key(block):
	english="QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm,.';:; -_"
	key=''
	for x in block:
		max_alpha=0
		char=''
		for i in range(32,127):
			alpha=0
			srring=xor_strings(x,len(x)*chr(i))
			for ch in srring:
				if ch in english:
					alpha+=1
			if (alpha>max_alpha):
				max_alpha=alpha
				char=chr(i)
		key+=char
	return key

def main():
	print "writing the plain test in \"./6out.txt\" ....."
	data = r.read().decode('base64')
	
	keysize=smallest_normalized_keysize(data)
	block=transposed_blocks(data,keysize)
	key=get_the_key(block)
	w.write(xor_strings(data,((len(data)/len(key))+2)*key))

	r.close()
	w.close()



if __name__ == '__main__':
    main()

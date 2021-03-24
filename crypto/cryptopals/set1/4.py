
r = open("4.txt", "r")
w = open("4out.txt", "w")


def xor_strings(xs, ys):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))
english="QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm,.\n\t\"';:; -_"
for x in r:
	binary_a = x.strip().decode("hex")
	for i in range(0,128):
		srring=xor_strings(binary_a,30*chr(i))
		if(all(ord(c) < 128 for c in srring)):
			w.write(srring+"\n")
			#final result
			if(all(ch in english for ch in srring)):
				print(srring,x,i,chr(i))
			
r.close()
w.close()		

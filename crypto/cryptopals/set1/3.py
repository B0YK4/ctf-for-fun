a='1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
binary_a = a.decode("hex")


def xor_strings(xs, ys):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))

for i in range(97,122):
	print xor_strings(binary_a,34*chr(i))

for i in range(65,90):
	print xor_strings(binary_a,34*chr(i))


# cOOKING mcS LIKE A POUND OF BACON
# the key is "y"
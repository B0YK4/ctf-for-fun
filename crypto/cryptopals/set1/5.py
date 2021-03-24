#Implement repeating-key XOR

a="Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key="ICE"

def xor_strings(xs, ys):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))

decrypted=xor_strings(25*key,a)
print decrypted.encode("hex")
print xor_strings(25*key,decrypted)



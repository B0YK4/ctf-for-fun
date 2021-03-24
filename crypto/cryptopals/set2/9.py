#python 3
s=raw_input("enter your massege: ")
n=int(raw_input("padding length: "))
print (s+(n-len(s))*("\\x0"+str(hex(n-len(s)))[2:]))
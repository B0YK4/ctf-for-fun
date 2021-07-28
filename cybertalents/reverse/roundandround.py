encoded_flag=["726F756E", "CABEE660","DDC1997D" ,"AA93C38B" ,"87E21216"]
flag=''

for i in range(len(encoded_flag)):
	# bits rotate right
	tmp=hex((int(encoded_flag[i],16) >> i)|(int(encoded_flag[i],16) << (32 - i)) & 0xFFFFFFFF)[2:]

	# caser for alphabet with -i
	for j in range(0,8,2):
		char_ascii=int(tmp[j:j+2],16)
		if (char_ascii > ord('`') and char_ascii <=ord('z') ):
			flag+=chr((char_ascii - ord('a') - i) % 26 + ord('a'))
		elif(char_ascii > ord('@')) and (char_ascii <=ord('Z') ):
			flag+=chr((char_ascii - ord('A') - i) % 26 + ord('A'))
		else:
			flag+=chr(char_ascii)

print(flag)

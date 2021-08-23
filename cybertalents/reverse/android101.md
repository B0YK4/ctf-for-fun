# Android101

**Category:** Malware Reverse Engineering   **Level:** medium   **Points:** 100

challenge: [android101](https://cybertalents.com/challenges/malware/android101)

```sh
$ d2j-dex2jar -f android101.apk
```

by opening the jar file with JD-GUI

validate() function in MainActivity:

```java
String Validate(String paramString) {
    StringBuilder stringBuilder = new StringBuilder(paramString);
    for (byte b = 0; b < stringBuilder.length(); b++) {
      for (byte b1 = b; b1 < stringBuilder.length() - 1; b1++) {
        char c = stringBuilder.charAt(b1);
        stringBuilder.setCharAt(b1, stringBuilder.charAt(b1 + 1));
        stringBuilder.setCharAt(b1 + 1, c);
      } 
    } 
    if (stringBuilder.toString().equals(String.valueOf(new char[] { 
            'l', 'g', 'c', 'n', 'y', 'u', 'r', 'V', 'r', '3', 
            '4', 'd', '0', 'D', 'f', '{', '_', '_', '3', '_', 
            'R', '}', '4', '3', 'n', 'a', '5', '0', '1' })))
      Toast.makeText(getApplicationContext(), String.valueOf(new char[] { 'C', 'o', 'r', 'r', 'e', 'c', 't' }, ), 1).show();
```

**solution:** doing the reverse of validate function

```py
l=['l', 'g', 'c', 'n', 'y', 'u', 'r', 'V', 'r', '3', '4', 'd', '0', 'D', 'f', '{', '_', '_', '3', '_', 'R', '}', '4', '3', 'n', 'a', '5', '0', '1']

for i in range(len(l),-1,-1):
	for j in range(len(l)-1,i,-1):
		c=l[j]
		l[j]=l[j-1]
		l[j-1]=c

print ''.join(l)
```

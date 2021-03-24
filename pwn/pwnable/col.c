#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
		res += ip[i];
		printf("int ip: %ss\n",ip[i]);
	}
	printf("%s\n",ip );
	printf("passcode: %d\n",res );
	return res;
}

int main(int argc, char* argv[]){
	if(argc<2){
		printf("usage : %s [passcode]\n", argv[0]);
		return 0;
	}
	printf("%s\n",argv[1] );
	if(strlen(argv[1]) != 20){
		printf("passcode length should be 20 bytes\n");
		return 0;
	}
	printf("hachcode: %d\n",hashcode );
	if(hashcode == check_password( argv[1] )){
		system("/bin/cat flag");
		return 0;
	}
	else
		printf("wrong passcode.\n");
	return 0;
}
//hashcode int =568134124
/*
solution is input a string that the sum of int of each 4 byte == hashcode
so we need 5 blocks each block sum = 568134124/5

   int         hex
113626824 = 0x06c5cec8
113626824
113626824
113626824
113626828 = 0x06c5cecc
---------
568134124

so we input each block as big indian hex using python
$ ./col "`python -c 'print(4*"\xc8\xce\xc5\x06"+"\xcc\xce\xc5\x06")'`"

*/
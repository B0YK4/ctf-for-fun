#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
	if(argc<2){
		printf("pass argv[1] a number\n");
		return 0;
	}
	int fd = atoi( argv[1] ) - 0x1234;
	printf("%d",fd);
	int len = 0;
	len = read(fd, buf, 32);
	printf("%d",len);
	printf("%s",buf);
	if(!strcmp("LETMEWIN\n", buf)){
		printf("good job :)\n");
		system("/bin/cat flag");
		exit(0);
	}
	printf("learn about Linux file IO\n");
	return 0;

}
/* solution is learn about file directors in linux
$ ./fd 4660
LETMEWIN
$
----------------
that make read fun to read from system fd index 0 which means stdin
*/
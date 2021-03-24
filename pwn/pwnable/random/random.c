#include <stdio.h>

int main(){
        unsigned int random;
        random = rand();        // random value!

        unsigned int key=0;
        scanf("%d", &key);
        printf("%d\n",random );

        if( (key ^ random) == 0xdeadbeef ){
                printf("Good!\n");
                system("/bin/cat flag");
                return 0;
        }

        printf("Wrong, maybe you should try 2^32 cases.\n");
        return 0;
}
/* rand() always returns the same value random=1804289383
so if the input key =(0xdeadbeef^random) then key^random will eq 0xdeadbeef
*/
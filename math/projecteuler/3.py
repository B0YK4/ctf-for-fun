num = 600851475143
i = 1
arr = [1]
while num != 1:
    i += 1
    for j in range(2, i):
        if(i % j == 0 or num % i == 0 or num < i):
            break
        x = num/i
        for k in xrange(2, x):
            if x % k == 0:
                break
            else:
                num /= i
                arr.append(i)

    print arr, num
#not done

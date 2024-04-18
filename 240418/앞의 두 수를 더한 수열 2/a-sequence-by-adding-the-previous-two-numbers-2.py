import sys

n = int(input())
if n == 1 or 2:
    print(1)
    sys.exit()


fib = [0]*(n+1)
fib[1] = 1
fib[2] = 1

for i in range(3, n+1):
    fib[i] = fib[i-1] + fib[i-2]

print(fib[n])
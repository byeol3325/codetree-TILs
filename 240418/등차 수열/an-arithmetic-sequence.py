n, a, b = map(int, input().split())
Arr = list(map(int, input().split()))

cnt = 0; now = 0
for i in range(len(Arr)):
    if Arr[i] == a:
        now = a
        cnt += 1
    elif Arr[i] == now + b and now != 0:
        now = Arr[i]
        cnt += 1

print(cnt)
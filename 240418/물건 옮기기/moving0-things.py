location = {}

n = int(input())
cnt = 0
for _ in range(n):
    loc, LR = map(int, input().split())
    if loc not in location:
        location[loc] = LR
    else:
        if location[loc] == LR:
            continue
        else:
            cnt += 1
            location[loc] = LR

print(cnt)
n, k = map(int, input().split())

max_ = 1
for _ in range(k):
    h, w = map(int, input().split())
    max_ = max(h*w, max_)

print(n//max_ + 1 )
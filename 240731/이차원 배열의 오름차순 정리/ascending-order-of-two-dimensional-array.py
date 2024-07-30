n = int(input())
k = int(input())

# n*n, A[i][j] = i*j (i, j : 1~n)
# 1 2 3 4 5 
# 2 4 6 8 10
# 3 6 9 12 15
# 4 8 12 16 20
# 5 10 15 20 25

# 1
# 1 2 2 4
# 1 2 2 3 3 4 6 6 9
# 1 2 2 3 3 4 4 4 6 6 8 8 9 12 12 16
# 1 2 2 3 3 4 4 4 5 5 6 6 8 8 9 10 10 12 12 15 15 16 20 20 25

def count_less_equal(x, n):
    cnt = 0
    for i in range(1, n+1):
        cnt += min(x//i, n)
    return cnt

left, right = 1, n*n
while left < right:
    mid = (left+right)//2
    if count_less_equal(mid, n) < k:
        left = mid+1
    else:
        right = mid

print(left)
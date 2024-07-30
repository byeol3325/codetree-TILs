n, m = map(int, input().split())
arr = [0]*n
for i in range(n):
    arr[i] = int(input())

def parametric_search(arr: list, m: int):
    left = 0
    right = sum(arr)//m
    n = len(arr)

    if right == 0:
        return 0

    Ks = [0]
    while left <= right:
        mid = (left + right) // 2

        cnt = 0
        for i in range(n):
            cnt += arr[i] // mid
        
        if cnt < m:
            # 더 크게할 수 있음 = 나누는 mid를 줄여야함
            right = mid-1
        elif cnt >= m:
            # 더 잘게 해야함 = 나누는 mid를 키워야함
            left = mid+1
            Ks.append(mid)
        
    """
    mid = (left + right) // 2
    cnt = 0
    for i in range(n):
        cnt += arr[i] // mid

    if cnt >= m:
        Ks.append(mid)
    """
    return max(Ks)


k = parametric_search(arr, m)
print(k)
# 3이나 5의 배수는 Moo
N = int(input())

"""
MAX = 10**9

cnt = 0
for i in range(1, MAX):
    if i % 3 == 0 or i % 5 == 0:
        continue
    cnt += 1

    if cnt == N:
        print(i)
        break
"""


arr = [1, 2, "Moo", 4, "Moo", "Moo", 7, 8, "Moo", "Moo", 11, "Moo", 13, 14, "Moo"] # 15에서 8개가 숫자

left = 1
right = N*2
answer = 0

# 1번 풀이
answer += 15 * (N//8)
dict_num = {1:1, 2:2, 3:4, 4:7, 5:8, 6:11, 7:13, 8:14}
answer += dict_num[N%8]

print(answer)
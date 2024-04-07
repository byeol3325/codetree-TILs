import sys
from collections import deque

input = sys.stdin.readline
dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]

n, m = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(n)]
base = []
for i in range(n):
    for j in range(n):
        if a[i][j] != 0:
            base.append([i, j])

cu = [0] * m
for i in range(m):
    x, y = map(int, input().split())
    cu[i] = [x-1, y-1]

base_start = []
ex = [[0] * n for _ in range(n)]
for x, y in cu:
    q = deque()
    q.append([x, y])
    ex[x][y] = 1
    check_mov = [[0] * n for _ in range(n)]
    check_mov[x][y] = 1
    flag = 0
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if 0 <= nx < n and 0 <= ny < n:
                if check_mov[nx][ny] == 0 and ex[nx][ny] == 0:
                    if a[nx][ny] == 1:
                        ex[nx][ny] = 1
                        base_start.append([nx, ny])
                        flag = 1
                    else:
                        q.append([nx, ny])
                        check_mov[nx][ny] = 1
            if flag:
                break
        if flag:
            break

ex = [[0] * n for _ in range(n)]
check_mov = [[[0] * m for _ in range(n)] for _ in range(n)]
check_end = [0] * m
cnt, idx = 1, 1
q = deque()
bx, by = base_start[0][0], base_start[0][1]
q.append([bx, by, 0])
ex[bx][by] = 1
check_mov[bx][by][0] = 1
while q:
    if 0 < idx < m:
        bx, by = base_start[idx][0], base_start[idx][1]
        ex[bx][by] = 1
        check_mov[bx][by][idx] = 1
    qlen = len(q)
    cnt += 1
    for _ in range(qlen):
        x, y, i = q.popleft()
        if check_end[i] == 1:
            continue
        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]
            if 0 <= nx < n and 0 <= ny < n:
                if check_mov[nx][ny][i] == 0 and ex[nx][ny] == 0:
                    if nx == cu[i][0] and ny == cu[i][1]:
                        ex[nx][ny] = 1
                        check_end[i] = 1
                    else:
                        q.append([nx, ny, i])

    if 0 not in check_end:
        break
    if 0 < idx < m:
        q.append([bx, by, idx])
    idx += 1

print(cnt)
import sys
from collections import deque

input = sys.stdin.readline
dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0] # 우선순위 고려 (상좌우하)

######################## 초기 값 설정 ########################
N, M = map(int, input().split()) 
matrix = [0] * N # matrix 값 저장
base_camps = [] # base_camp 위치들 저장
for i in range(N):
    line = list(map(int, input().split()))
    for j in range(N):
        if line[j] == 1:
            base_camps.append([i, j])
    matrix[i] = line

stores = [0] * M # store 위치 저장
for i in range(M):
    x, y = map(int, input().split())
    stores[i] = [x-1, y-1] # 위치 보정. 0,0에서 시작해서 -1, -1 해줘야함
#############################################################


base_start = []
ex = [[0] * N for _ in range(N)] # 도착하면 이제 안 움직임
for x, y in stores:
    q = deque()
    q.append([x, y])
    ex[x][y] = 1
    check_mov = [[0] * N for _ in range(N)]
    check_mov[x][y] = 1
    flag = 0
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if 0 <= nx < N and 0 <= ny < N:
                if check_mov[nx][ny] == 0 and ex[nx][ny] == 0:
                    if matrix[nx][ny] == 1:
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

ex = [[0] * N for _ in range(N)]
check_mov = [[[0] * M for _ in range(N)] for _ in range(N)]
check_end = [0] * M
cnt, idx = 1, 1
q = deque()
bx, by = base_start[0][0], base_start[0][1]
q.append([bx, by, 0])
ex[bx][by] = 1
check_mov[bx][by][0] = 1
while q:
    if 0 < idx < M:
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
            if 0 <= nx < N and 0 <= ny < N:
                if check_mov[nx][ny][i] == 0 and ex[nx][ny] == 0:
                    if nx == stores[i][0] and ny == stores[i][1]:
                        ex[nx][ny] = 1
                        check_end[i] = 1
                    else:
                        q.append([nx, ny, i])

    if 0 not in check_end:
        break
    if 0 < idx < M:
        q.append([bx, by, idx])
    idx += 1

print(cnt)
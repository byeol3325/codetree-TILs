# n번 사람은 n분에 각자 베이스캠프에서 출발하여 편의점으로
# 총 m명이 빵 구하기
# 출발 전 격자 밖에 있음. 목표하는 편의점 모두 다름

# 순서대로 진행됨
# rule 1. 모두 본인이 가고 싶은 편의점 향해서 1칸. 상좌우하 우선순위
#         최단거리란 상하좌우로 최소칸
# rule 2. 편의점 도착시 편의점에서 멈춤. 이때부터 다른 사람들은 해당 편의점 칸 못 지나감
# rule 3. 현재 t분이고 t <= m을 만족한다면 t 번 사람은 자신이 가고 싶은 편의점과 가장 가까이 있는 베이스캠프에 들어감
#         가까운 베이스캠프가 여러가지 경우 행이 작고 열이 작은 베이스캠프로
#         t번 사람이 베이스 캠프로 이동하는데 시간이 전혀 소요되지 않음
#         이때부터 해당 베이스캠프 칸 지날 수 없음. t번 사람이 편의점 향해 움직이기 시작했더라도 해당 베이스캠프는 지나갈 수 없음

import sys
input = sys.stdin.readline

from collections import deque

N, M = map(int, input().split())
matrix = [list(map(int, input().split())) for _ in range(N)]
base_camps = []
for i in range(N):
    for j in range(N):
        if matrix[i][j] == 1:
            base_camps.append([i,j])

stores = [list(map(int, input().split())) for _ in range(M)]
people = deque() # person : (x,y, num, end) end == 1이면 끝 or 없애기?

dy = [-1,0,0,1]; dx = [0,-1,1,0] # 상좌우하 우선순위
def Go(people):
    global matrix, stores
    n_people = deque()
    while people:
        y, x, num = people.popleft()
        #print("Before : ", y, x, num)
        #print("STORE : ", stores[num-1])
        min_idx = -1; min_d = float("inf")
        #어디로 갈지 정하기
        for i in range(4):
            ny = y + dy[i]; nx = x + dx[i]
            if 0<=ny<N and 0<=nx<N and matrix[ny][nx] == 2: # 못가는 곳임 ㅅㄱ (basecamp시작 or store 도착)
                continue
        
            nd = abs(ny-stores[num-1][0]) + abs(nx-stores[num-1][1]) #최단거리로
            if min_d > nd:
                min_d = nd
                min_idx = i
            #print("AFTER : ", ny, nx, nd)
        
        ny = y+dy[min_idx]; nx = x+dx[min_idx]
        if min_d == 0: #도착한거임 덜덜
            matrix[ny][nx] = 2 #이제 못지나감
            continue
        n_people.append([ny, nx, num])
    
    return n_people

def Find_camp(num): #num에 time으로 들어올거임
    global base_camps, stores
    store = stores[num-1] # num에 맞는 store 위치
    store[0]-=1; store[1]-=1; # 격자 맞춰줘야함

    distances = [] # 최소거리 구하기 위해 모든 거리 구하기
    for bc in base_camps:
        dist = abs(bc[0] - store[0]) + abs(bc[1] - store[1])
        distances.append(dist)
    
    min_dis = min(distances) # 최소거리
    #최소거리 여러개인지 확인, base_camps(idx), idx
    min_dis_loc = [base_camps[i]+[i] for i, d in enumerate(distances) if d == min_dis]
    min_dis_loc.sort() # 여러개면 우선순위
    base_camps.pop(min_dis_loc[0][2])
    return min_dis_loc[0][:2] + [num] # loc

time_ = 0
while True:
    # 일단 m초까지 실행해서 모든 사람 있도록.
    time_ += 1 # 1초 실행

    people = Go(people) # 사람들 대이동 ㄷㄷ
    
    if time_ <= M: # m초전까지는 사람들 계속 들어옴
        # 어느 베이스캠프에서 시작할지 정하기
        person = Find_camp(time_); matrix[person[0]][person[1]] = 2 #어디서 시작할지 정하고 거기 이제 못감 ㅅㄱ
        people.append(person)
    
    # 시간 m지나고 people 비면 finish
    if time_ > M and len(people) == 0: # 베이스캠프와 편의점 위치가 겹치지 않으므로 최소 시간은 m보다 큼
        break
    
    #if time_ == 7:
    #    print(people)
    #    break

print(time_)
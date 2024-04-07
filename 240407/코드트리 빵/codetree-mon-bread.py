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
matrix = [] # 격자 정보
base_camps = [] # base 캠프 어딨노
for i in range(N):
    line = list(map(int, input().split()))
    for j in range(N):
        if line[j] == 1: # 베이스캠프 위치
            base_camps.append([i,j])
    matrix.append(line)

stores = [0] * M # storestore
for i in range(M):
    y, x = map(int, input().split())
    stores[i] = [y-1,x-1] # 격자 맞추기. 1,1이 아닌 0,0에서 시작
fin_ = [0] * M # 그 사람 다 끝났는지 확인
start_ = [0] * M # 각 사람들 어디서 스타트하는지. m store가기 위한 사람들
people = deque() # person : (x,y, num) 다하면 없애기

dy = [-1,0,0,1]; dx = [0,-1,1,0] # 상좌우하 우선순위
check_mov = [[[0]*M for _ in range(N)] for _ in range(N)]
def Go():
    global matrix, stores, people, fin_, check_mov
    n_people = len(people)
    for _ in range(n_people):
        y, x, num = people.popleft()
        if fin_[num] == 1: # 끝난놈들은 빼기
            continue
        #print("Before : ", y, x, num)
        #print("STORE : ", stores[num-1])
        #print("PEOPLE : ", y, x, num, stores[num])
        #dis = abs(y-stores[num][0]) + abs(x-stores[num][1])
        #어디로 갈지 정하기
        for i in range(4):
            ny = y + dy[i]; nx = x + dx[i]
            if 0<=ny<N and 0<=nx<N: # 안에 있는지
                pass
            else: # 없으면 나가잇!
                continue
            
            if matrix[ny][nx] == 2: # 못가는 곳임 ㅅㄱ (basecamp시작 or store 도착)
                continue
            
            if check_mov[ny][nx][num] == 0: # 갈 수 있는데
                if stores[num] == [ny, nx]: # 도착한거임
                    matrix[ny][nx] = 2 # 이제 못지나감
                    fin_[num] = 1 # 다 끝
                    break
                people.append([ny, nx, num]) # 일단 이동할 수 있는 곳들 정리
                check_mov[ny][nx][num] = 1 # 방문해봄
            #nd = abs(ny-stores[num][0]) + abs(nx-stores[num][1]) # 거리 비교해야함
            #print("Here : ", dis, nd)
            #if dis > nd: # 짧은 곳 있으면 거기로 바로 ㄱ
            #    people.append([ny, nx, num])
            #    break
            #people.append([ny, nx, num]) # 갈데가 없으니 일단 이동할 수 있는 것들 정리
            #print("AFTER : ", ny, nx, nd)
    return

def Find_camp():
    global base_camps, stores, start_, N, M, matrix

    ex = [[0]*N for _ in range(N)]
    for i in range(M):
        #print("HERE : ", i)
        store = stores[i]
        ex[store[0]][store[1]] = 1 # store 마다 자리 차지 빼기
        check_q = [[0]*N for _ in range(N)]
        q = deque()
        q.append(store)
        done = 0
        while q:
            [y, x] = q.popleft()
            check_q[y][x] = 1 # 간 자리 빼기
            #print("HERE : ", i, y, x)
            for j in range(4):
                ny = y + dy[j]; nx = x + dx[j]
                if 0<= ny < N and 0<= nx < N: # 안에 있는지
                    if check_q[ny][nx] == 0 and ex[ny][nx] == 0: # 갈 수 있는지
                        if matrix[ny][nx] == 1: # 최단거리에 store가 있음
                            start_[i] = [ny, nx] # 어디서 시작할지
                            ex[ny][nx] = 1
                            done = 1
                        else:
                            q.append([ny, nx])
                if done == 1:
                    break
            if done == 1:
                break
        
        #break
    return

Find_camp() # 각자 어디서 시작할지 위치 찾기 
#print(start_)

time_ = 0
while True:
    # 일단 m초까지 실행해서 모든 사람 있도록.
    Go() # 사람들 대이동 ㄷㄷ
    
    time_ += 1
    if time_ <= M: # m초전까지는 사람들 계속 들어옴
        # 어느 베이스캠프에서 시작할지 정하기
        person = start_[time_-1]
        matrix[person[0]][person[1]] = 2 # 추가되면 못가는곳으로 바꾸기
        people.append(person + [time_-1]) # 사람 추가됨
        check_mov[person[0]][person[1]][time_-1] = 1
    
    # 시간 m지나고 people 비면 finish
    if len(people) == 0 or sum(fin_) == M: # 베이스캠프와 편의점 위치가 겹치지 않으므로 최소 시간은 m보다 큼
        break
    
    #print("TIME : ", time_)
    #for i in range(N):
    #    print(matrix[i])
    #print(people)
    #if time_ == 55:
    #    print(people)
    #    print(fin_)
        #for i in range(N):
        #    print(matrix[i])
        break
print(time_)
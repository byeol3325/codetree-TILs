from collections import deque
import heapq as hq

N, M, K = map(int, input().split())
turrets = [] # turret = [score, cnt, (r+c), c]
# max -> turrets, turrets -> max로 어떻게 업데이트 시켜줄거냐....

matrix = []
for i in range(N):
    line = list(map(int, input().split()))
    for j in range(M):
        if line[j] > 0:
            turrets.append([line[j], 0, i+j, j])
    matrix.append(line)
turrets.sort()

cnt_matrix = [[0]*M for _ in range(N)]

# 1. 공격자 선정.
#       공격력 1이상에서 가장 약한 포탑으로 공격자 선정. 핸디캡 N+M 만큼 공격력 증가
#       선정기준 우선순위 1) 공격력 젤 낮은거 2) 가장 최근에 공격한 포탑(모든 포탑은 시점 0에 모두 공격한 경험이 있다 가정.) 3) 행+열이 큰 포탑. 4) 열(column) 값이 큰거

# 2. 공격!
#       자신을 제외한 가장 강한 포탑 공격.
#       가장 강한 포탑 선정 우선순위 1) 공격력이 가장 높은 포탑 2) 공격한지 가장 오래된 포탑 3) 행+열이 가장 작은 포탑  4) 열 값이 가장 작은 포탑
#    1] 레이저 공격
#       -1: 상하좌우 4개 방향. 막히면 반대편으로 나옴
#       -2: 부서진 포탑있는 곳으론 지날 수 없음 (공격력 0 이하)
#       최단 경로로 공격하며 최단 경로가 없으면 :포탄 공격으로"
#       우/하/좌/상 우선순위대로 경로 선택
#       공격시 공격자의 공격력만큼 피해 입음. 경로는 절반만큼 공격 받음

#   2] 포탄 공격
#   공격자의 공격력만큼 피해 입음. 주위 8개도 절반만큼 피해 받음. //2
#   공격자는 해당 공격에 영향X
#   가장자리시 반대로 나옴. 레이저와 같음

def ShowINFO():
    print("=============MATRIX=============")
    for i in range(N):
        print(matrix[i])
    print("=============CNT MATRIX=============")
    for i in range(N):
        print(cnt_matrix[i])
    print("=============TURRETS=============")
    print(turrets)
    
def FindAttacker():
    return turrets[0]

def Findtarget():
    return turrets[-1]

def go(next_):
    global N, M
    next_[0] = next_[0]%N
    next_[1] = next_[1]%M
    return next_

def ATTACK(attacker, target):
    path = LaserPath(attacker, target)
    if path == False: # 레이저 공격 루트가 없으면 포격 공격으로 가야지
        path = BoomPath(attacker, target)
    ATTACKPATH(attacker, path)
    return

def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

dr = [0,1,0,-1, 1,1,-1,-1]; dc = [1,0,-1,0, 1,-1,1,-1] # 우하좌상우선순위
def LaserPath(attacker, target):
    global N, M, dr, dc
    start_ = [attacker[2]-attacker[3], attacker[3]]; matrix[start_[0]][start_[1]] += N+M # 포탑 공격력 보정
    end_ = [target[2]-target[3], target[3]]
    dis_ = distance(start_, end_)
    # 1,2 [1,3],[1,3
    q = deque(); q.append([start_]) # r,c
    #print("HERE : ", q)
    visited = [[0]*M for _ in range(N)]
    while q:
        #print("HERE q : ", q)
        path = q.popleft()
        r, c = path[-1][0], path[-1][1]
        visited[r][c] = 1
        for i in range(4):
            nr = r+dr[i]; nc = c+dc[i]
            next_ = go([nr, nc])
            #print("HERE next_ : ", next_)
            if [nr, nc] == end_: # 도착!
                return path + [next_] # 도착 경로
            
            if matrix[next_[0]][next_[1]] > 0 and distance(end_, next_) < distance(end_, [r,c]): # 길이 있고 가까워지면
                q.append(path + [next_])

    return False # 도착못해서 False

def UPDATETURRETS():
    global turrets, N, M, cnt_matrix
    turrets = [] # turret = [score, cnt, (r+c), c]
    for i in range(N):
        for j in range(M):
            if matrix[i][j] > 0: # 0 이상인 경우만 다시 터렛 업데이트
                turrets.append([matrix[i][j], cnt_matrix[i][j], (i+j), j])
            else:
                matrix[i][j] = 0
    turrets.sort()
    return

def ATTACKPATH(attacker, path):
    global matrix, cnt_matrix
    len_path = len(path)
    cnt_matrix[path[0][0]][path[0][1]] += 1 # 공격자 횟수 추가
    
    score = matrix[attacker[2]-attacker[3]][attacker[3]]

    for n in range(N):
        for m in range(M):
            if [n, m] == path[0]: # 공격자
                continue
            elif [n, m] == path[-1]: # 포격 받은 곳
                matrix[n][m] -= score
            elif [n, m] in path: # 포격 받은 경로
                matrix[n][m] -= score//2
            elif matrix[n][m] > 0: # 포격 받지 않은 지역
                matrix[n][m] += 1
    
    UPDATETURRETS()
    return

def BoomPath(attacker, target):
    global N, M, dr, dc
    start_ = [attacker[2]-attacker[3], attacker[3]]
    end_ = [target[2]-target[3], target[3]]
    q = deque(); q.append([start_])
    for i in range(8):
        side_ = [end_[0]+dr[i], end_[1]+dc[i]]
        if side_ == start_: # 시작점 제외
            continue
        q.append([side_])
    q.append([end_])
    return



# =======================
#ShowINFO()

stop = -1
for k in range(K):
    if len(turrets) <= 1: # 남은 포탑이 1개 이하면 다 제거
        break

    if k == stop:
        print("TURN : ", k)
    # 공격자, 공격 받을자 선정
    attacker = FindAttacker() # 공격자
    target = Findtarget() # 목표 지점

    #print(attacker)
    #print(target)
    ATTACK(attacker, target)# 공격! 및 업데이트

    
    if k == stop:
        ShowINFO()
        break

print(turrets[-1][0])
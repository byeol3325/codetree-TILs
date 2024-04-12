from collections import deque
import heapq as hq

N, M, K = map(int, input().split())
turrets = [] # turret = [power 작, 순서 커, r+c커, c커] [score, 최근에 공격한, (r+c), c] 
            # attacked = [score 커, 순서 작, (r+c)작, c작]
matrix = []
for i in range(N):
    line = list(map(int, input().split()))
    for j in range(M):
        if line[j] > 0:
            hq.heappush(turrets, [line[j], 0, -(i+j), -j])
            #turrets.append([line[j], 0, -(i+j), -j])
    matrix.append(line)
#turrets.sort()

#cnt_matrix = [[0]*M for _ in range(N)]

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
    #print("=============CNT MATRIX=============")
    #for i in range(N):
    #    print(cnt_matrix[i])
    print("=============TURRETS=============")
    print(turrets)
    
def FindAttacker():
    return turrets[0]

def Findtarget():
    return sorted(turrets, key = lambda x:(-x[0], -x[1], -x[2], -x[3]))[0]

def go(next_):
    global N, M
    next_[0] = next_[0]%N
    next_[1] = next_[1]%M
    return next_

# turret = [score, 3000-k, -(r+c), -c]
def ATTACK(attacker, target, k):
    path = LaserPath(attacker, target)
    #print("PATH LASER : ", path)
    if path == False: # 레이저 공격 루트가 없으면 포격 공격으로 가야지
        path = BoomPath(attacker, target)
        #print("PATH BOOM, attacker, target : ", path, attacker, target)
    #print("PATH : ", path)
    ATTACKPATH(attacker, path, k)
    return

def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

# turret = [score, 3000-k, -(r+c), -c]
dr = [0,1,0,-1, 1,1,-1,-1]; dc = [1,0,-1,0, 1,-1,1,-1] # 우하좌상우선순위
def LaserPath(attacker, target):
    global N, M, dr, dc
    start_ = [-attacker[2]+attacker[3], -attacker[3]]; matrix[start_[0]][start_[1]] += N+M # 포탑 공격력 보정
    end_ = [-target[2]+target[3], -target[3]]
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
            if next_ == end_: # 도착!
                return path + [next_] # 도착 경로
            
            if matrix[next_[0]][next_[1]] > 0 and distance(end_, next_) < distance(end_, [r,c]): # 길이 있고 가까워지면
                q.append(path + [next_])
        #print("LASER PATH, end : ", q, end_)
    return False # 도착못해서 False

# turret = [score, 3000-k, -(r+c), -c]
def UPDATETURRETS(k):
    global turrets, N, M
    turrets = [] # turret = [score, cnt, (r+c), c]
    for i in range(N):
        for j in range(M):
            if matrix[i][j] > 0: # 0 이상인 경우만 다시 터렛 업데이트
                hq.heappush(turrets, [matrix[i][j], -k, -(i+j), -j])
                #turrets.append([matrix[i][j], 3000-cnt_matrix[i][j], -(i+j), -j])
            else:
                matrix[i][j] = 0
    turrets.sort()
    return

# turret = [score, 3000-k, -(r+c), -c]
def ATTACKPATH(attacker, path, k):
    global matrix
    
    score = matrix[-attacker[2]+attacker[3]][-attacker[3]]
    for n in range(N):
        for m in range(M):
            if [n, m] == path[0]: # 공격자
                #print("ATTACKER", [n, m])
                continue
            elif [n, m] == path[-1]: # 포격 받은 곳
                matrix[n][m] -= score
            elif [n, m] in path: # 포격 받은 경로
                matrix[n][m] -= score//2
            elif matrix[n][m] > 0: # 포격 받지 않은 지역
                matrix[n][m] += 1
    
    UPDATETURRETS(k)
    return

# turret = [score, 3000-k, -(r+c), -c]
def BoomPath(attacker, target):
    global N, M, dr, dc
    #print("START BOOMPATH")
    start_ = [-attacker[2]+attacker[3], -attacker[3]]
    end_ = [-target[2]+target[3], -target[3]]
    q = deque(); q.append(start_)
    for i in range(8):
        side_ = [end_[0]+dr[i], end_[1]+dc[i]]
        side_ = go(side_)
        #print("SIDE : ", side_)
        if side_ == start_ or matrix[side_[0]][side_[1]] == 0: # 시작점과 없는 곳 제외
            continue
        q.append(side_)
    q.append(end_)
    #print("BOOM : " , q)
    return q



# =======================
#ShowINFO()

#print("=================================")
stop = -1
for k in range(1, K+1):
    if len(turrets) <= 1: # 남은 포탑이 1개 이하면 다 제거
        break

    if k == stop:
        print("TURN : ", k)
    # 공격자, 공격 받을자 선정
    attacker = FindAttacker() # 공격자
    #cnt_matrix[-attacker[2]+attacker[3]][-attacker[3]] = k # 마지막 공격을 언제 했는지
    
    target = Findtarget() # 목표 지점

    if k == stop:
        print("attacker : ", attacker)
        print("target : ", target)
    ATTACK(attacker, target, k)# 공격! 및 업데이트

    if k == stop:
        ShowINFO()
        break

ans = 0
for i in range(N):
    for j in range(M):
        ans = max(ans, matrix[i][j])
print(ans)
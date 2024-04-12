# 각 기사들 정보.
# 받은 데미지, 위치
from collections import deque
import copy

L, N, Q = map(int, input().split()) # L:체스판가로세로, N:기사수, Q:명령수

trap = []
wall = []
board = []
board.append([0]*(L+1))
for i in range(1, L+1):
    line = list(map(int, input().split()))
    for j in range(1, L+1):
        if line[j-1] == 1:
            trap.append([i,j])
        elif line[j-1] == 2:
            wall.append([i,j])
    board.append([0] + line)

knights = {} # i:knight
class knight:
    def __init__(self, r,c,h,w, life, damage=0):
        self.r = r
        self.c = c
        self.h = h
        self.w = w
        self.life = life
        self.damage = damage
    
    def get_damage(self, d):
        self.life -= d
        self.damage += d

for i in range(1, N+1):
    info = list(map(int, input().split())) # r, c, h, w, k
    knights[i] = knight(info[0], info[1], info[2], info[3], info[4])
    r,c,H,W = info[0],info[1],info[2],info[3]
    for h in range(H):
        for w in range(W):
            board[r+h][c+w] += 10*i
    #print("knights(i, r, c, h, w, k) : ",i, r,c,H,W )


def Check(ith, d):
    global knights, board
    move_knights = {}
    move_knights[ith] = 0 # ith:damage
    
    # 확인
    q = deque(); q.append(ith)
    #k = 0
    while q:
        mov_ith = q.popleft()
        damage = 0
        move_locations = []
        if knights[mov_ith].life <=0: # 죽은놈 고려X . 혹시 몰라서 넣음
            continue

        r,c,H,W = knights[mov_ith].r, knights[mov_ith].c, knights[mov_ith].h, knights[mov_ith].w
        for h in range(H):
            for w in range(W):
                move_locations.append([r+h, c+w])
        #print("move_locations, d : ", move_locations, d)
        for r,c in move_locations:
            nr, nc = r+d[0], c+d[1]
            #print("nr, nc : ", nr, nc)
            if 1<=nr<=L and 1<=nc<=L: # 일단 격자 안
                if board[nr][nc] == 2: # 벽 있어서 못 움직임
                    #print("WALL!!!!")
                    return False
                if board[nr][nc]%10 == 1: # 함정이 있음
                    damage += 1
                
                if board[nr][nc]//10 >= 1: # 어떤 기사가 있어
                    #print("ADD : ", board[nr][nc]//10)
                    if board[nr][nc]//10 == mov_ith: # 해당 그 기사 영역이라 무시
                        continue
                    
                    q.append(board[nr][nc]//10) # 기사 추가
                    move_knights[board[nr][nc]//10] = 0
                    #move_knights.add(board[nr][nc]//10) # 기사 추가
            else: # 격자 밖이라 못 움직임
                #print("OUT!!!!")
                return False
        
        #print("GOOD MOVE KNIGHT : ", mov_ith)
        #print("GOOD MOVE KNIGHT : ", q)
        if mov_ith != ith:
            move_knights[mov_ith] = damage # 데미지 저장
        q = set(q) # 중복된 기사들 제거
        q = deque(q)
        #k+=1
        #if k == 3:
        #    break
    return move_knights

def Move(move_knights, d):
    global knights, board
    #print("move_knights : ", move_knights)
    if move_knights == False or move_knights == {}:
        return

    for k, v in move_knights.items(): # ith: damage
        knights[k].get_damage(v) # 데미지 먹음
        r,c,H,W = knights[k].r, knights[k].c, knights[k].h, knights[k].w
        for h in range(H):
            for w in range(W):
                board[r+h][c+w] -= 10*k # 일단 초기화
        #print("before k knight r c  : ", k, r, c)
        #print("initialize board : ")
        #for i in range(L+1):
        #    print(board[i])

        if knights[k].life <= 0: # 죽었으면 고려 X
            continue

        # 살아있는놈만 변경       
        knights[k].r += d[0]
        knights[k].c += d[1]
        r,c = knights[k].r, knights[k].c
        #print("after k knight new r c : ", k, r, c)
        for h in range(H):
            for w in range(W):
                board[r+h][c+w] += 10*k #보드 변경
    return

direction = [[-1,0], [0,1], [1,0], [0,-1]]
stop = -1
for i in range(1, Q+1):
    q = list(map(int, input().split()))
    ith, d = q[0], direction[q[1]]
    if i == stop:
        print("TURN : ", i)
    
    Move(Check(ith, d), d)

    if i == stop:
        print("=============== board : ")
        for i in range(L+1):
            print(board[i])
        break

total_damage = 0
for k, v in knights.items():
    if v.life <= 0:
        continue
    total_damage += v.damage
print(total_damage)


#print("=============== board : ")
#for i in range(L+1):
#    print(board[i])
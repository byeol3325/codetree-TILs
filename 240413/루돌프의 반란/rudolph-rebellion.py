N, M, P, C, D = map(int, input().split())
# N*N 보드, (r,c)-1~N. M개 턴. 산타 1~P번. C루돌프 힘. D 산타 힘
dr = [-1,0,1,0,1,-1,1,-1]; dc = [0,1,0,-1,1,1,-1,-1] #상우하좌 + 4대각
OUT_ = 0

class rudolf:
    def __init__(self, r,c, power, d=0):
        self.r = r
        self.c = c
        self.power = power
        self.d = d
    
    def getInfo(self):
        return [self.r, self.c, [dr[self.d], dc[self.d]]]

class santa:
    def __init__(self, idx, r,c, power, stun=0, out=0, score=0, d=0):
        self.idx = idx
        self.r = r
        self.c = c
        self.power = power
        self.stun = stun
        self.out = out
        self.score = score
        self.d = d

    def getInfo(self):
        if self.out == 1:
            return [self.idx, self.score]
        return [self.idx, self.r, self.c, self.stun, self.out, self.score, [dr[self.d], dc[self.d]]]
    
    def getScore(self, s):
        self.score += s
    
    def __lt__(self, other):
        if self.r != other.r:
            return self.r < other.r
        return self.c < other.c


board = [[0]*(N+1) for _ in range(N+1)]

line = list(map(int, input().split()))
R = rudolf(line[0], line[1], C)
board[line[0]][line[1]] = -1 # 루돌프 -1

santas = {}#산타 번호, 산타
for _ in range(P):
    line = list(map(int, input().split()))
    santas[line[0]] = santa(line[0], line[1], line[2], D)
    board[line[1]][line[2]] = line[0] # board 산타 id
#print("rudolf info (r,c, power) :", R.getInfo())
#for k, v in santas.items():
#    print(k, "santa info (idx, r,c, power) : ", v.getInfo())

def Distance(R, santa):
    return (R.r - santa.r)**2 + (R.c - santa.c)**2

def RGo():
    # 루돌프 움직임
    global santas, R, P, board
    
    board[R.r][R.c] = 0 # 루돌프 이동 전 제거
    # 가장 가까운 산타 찾기
    dis = float("inf")
    close_santa = None
    for k, v in santas.items(): #idx, santa
        if v.out == 1: # out 인 산타는 제외
            continue
        if dis > Distance(R, v): # 더 가까운 santa로 갱신
            dis = Distance(R, v); close_santa = v
        elif dis == Distance(R,v):
            if close_santa < v: # r이 더 큰, c가 더큰
                close_santa = v 
    
    # 루돌프 이동
    min_dis = float("inf"); min_dis_dir = -1
    for i in range(8):
        nr, nc = R.r+dr[i], R.c+dc[i]
        if min_dis > (nr-close_santa.r)**2 + (nc-close_santa.c)**2:
            min_dis = (nr-close_santa.r)**2 + (nc-close_santa.c)**2
            min_dis_dir = i
    
    R.r += dr[min_dis_dir]; R.c += dc[min_dis_dir] # 루돌프 이동시킴
    board[R.r][R.c] = -1 # 루돌프 board 위에서 이동시킴
    R.d = min_dis_dir # 루돌프 방향 갱신
    if min_dis == 0: # 루돌프-산타 충돌
        Collapse(R, close_santa, 'r')

def SantaGo():
    # 산타 움직임
    global dr, dc, board, santas, P
    for i in range(1, P+1):
        v = santas[i]
        if v.out == 1: #밖이면 고려X
            continue
        if v.stun > 0: # 이번 한 턴 쉬기
            v.stun -= 1
            continue
        
        dis = Distance(R, v) # 현재 산타와 루돌프 거리
        min_dis = dis; min_dis_dir = -1;
        for i in range(4):
            nr, nc = v.r+dr[i], v.c+dc[i]
            if 0<nr<=N and 0<nc<=N: # 내부
                if board[nr][nc] <= 0: # 다른 산타 없음 (루돌프가 있거나 빈곳)
                    if min_dis > (nr-R.r)**2 + (nc-R.c)**2: # 가까워지는 곳
                        min_dis = (nr-R.r)**2 + (nc-R.c)**2
                        min_dis_dir = i
            
        if min_dis_dir == -1: # 갈 곳이 없음. 다음 산타
            continue
        
        board[v.r][v.c] = 0 # 산타 이동 전 자리 제거
        v.r += dr[min_dis_dir]; v.c += dc[min_dis_dir] # 산타의 r,c 갱신
        v.d = min_dis_dir # 산타의 d 갱신
        if min_dis == 0: #산타가 루돌프에 충돌
            Collapse(R, v, 's')
        else: #산타 잘 이동함
            board[v.r][v.c] = v.idx
    return

def Collapse(R, santa, opt):
    global dr, dc, board, OUT_
    # 충돌
    if opt == 'r': #루돌프가 와서 충돌
        #board[santa.r][santa.c] = 0 # 부딪힌 곳이라 루돌프가 차지함
        santa.getScore(R.power) # 산타 C점 얻음
        santa.r += R.power*dr[R.d]; santa.c += R.power*dc[R.d] # 루돌프 온 방향으로 밀려남
        santa.d = R.d; santa.stun = 2 # 산타 방향 갱신, 부딪혀서 해당 산타 기절
        if santa.r <= 0 or santa.c <= 0 or santa.r >= N+1 or santa.c >= N+1: #밖임
            santa.out = 1 # 밖이라 out
            OUT_ += 1
        elif board[santa.r][santa.c] != 0: # 다른 산타가 있음
            #print("Interact r santa : ", santa.idx)
            Interact(santa, santas[board[santa.r][santa.c]])
        elif board[santa.r][santa.c] == 0: # 산타 없음
            board[santa.r][santa.c] = santa.idx # 산타 이동완료
            return
    else: # opt = 's' # 산타가 와서 충돌
        #print("collapse santa info : ", santa.idx, santa.r, santa.c)
        santa.getScore(santa.power) # 산타 D점 얻음
        santa.r -= santa.power*dr[santa.d]; santa.c -= santa.power*dc[santa.d] # 루돌프로 가려던 방향 반대로 밀려남
        santa.d = (santa.d+2)%4; santa.stun = 1 # 산타 방향 갱신, 부딪혀서 해당 산타 기절
        if santa.r <= 0 or santa.c <= 0 or santa.r >= N+1 or santa.c >= N+1: #밖임
            santa.out = 1 # 밖이라 out
            OUT_ += 1
        elif board[santa.r][santa.c] != 0: # 다른 산타가 있음
            #print("Interact santa : ", santa.idx)
            Interact(santa, santas[board[santa.r][santa.c]])
        elif board[santa.r][santa.c] == 0: # 산타 없음
            board[santa.r][santa.c] = santa.idx # 산타 이동완료
            return
    return

def Interact(s1, s2):
    # 상호작용 (s1이 와서 s2를 침)
    global dr, dc, board, N
    d = s1.d
    s2.r += dr[d]; s2.c += dc[d];
    board[s1.r][s1.c] = s1.idx # 1이 2 자리를 먹음
    if s2.r <= 0 or s2.c <= 0 or s2.r >= N+1 or s2.c >= N+1: #밖임
        s2.out = 1
        OUT_ += 1
    elif board[s2.r][s2.c] != 0: # 다른 산타가 있음
        #board[s2.r][s2.c] = s2.idx # 다른 산타가 앉음
        Interact(s2, board[s2.r][s2.c])
    elif board[s2.r][s2.c] == 0: # 산타가 없음
        board[s2.r][s2.c] = s2.idx # 산타 이동 완료
    return

def GetBonus():
    global santas
    for k, v in santas.items():
        if v.out == 0:
            v.getScore(1)
    return

# ========================

stop = -1
show_board = 1
show_rudolf = 1
show_santas = 1

if stop == 1:
    print("before : ")
    for i in range(1, N+1):
        print(board[i][1:])

for m in range(1, M+1):
    if OUT_ >= P: # 산타가 모두 탈락
        break
    if m == stop:
        print("========= round ", m)
        print("before : ")
        if show_board == 1:
            for i in range(1, N+1):
                print(board[i][1:])

    RGo()
    SantaGo()
    GetBonus()
    if m == stop:
        print("after : ")
        if show_board == 1:
            for i in range(1, N+1):
                print(board[i][1:])
        if show_rudolf == 1:
            print("rudolf info (r,c, d) :", R.getInfo())
        if show_santas == 1:
            for i in range(1, P+1):
                print(i, "santa info (idx, r,c, stun, out, score, d) : ", santas[i].getInfo())
        break

#print("rudolf info (r,c, power) :", R.getInfo())
for i in range(1, P+1):
    print(santas[i].score, end=" ")
import sys
input = sys.stdin.readline

def Dist(x1, x2):
    return (x1[0]-x2[0])**2 + (x1[1]-x2[1])**2

#N*N, (r,c) 
go = [[-1,0],[0,1],[1,0],[0,-1],[1,1],[1,-1],[-1,-1],[-1,1]] #상우하좌 + 4대각


N, M, P, C, D = map(int, input().split())
R = list(map(int, input().split()))
santas = [list(map(int, input().split()))+[0,0] for _ in range(P)] # 번호, Sr, Sc, score, stun
n = len(santas)
# stun: -1/0/1 ==> 탈락/정상/스턴먹음
out = 0

def RGo(R):
    global go, santas, n
    distances = []

    for i in range(n): # 어느게 가장 가까운 산타인지 찾기
        if santas[i][4] == -1: # 탈락이면 제외
            distances.append(float("inf"))
        else:
            distances.append(Dist(R, santas[i][1:3]))
    min_ = min(distances) # 가장 짧은거.
    min_idxs = [i for i in range(n) if distances[i] == min_] #여러개인지 확인
    min_santa = santas[min_idxs[0]]

    if len(min_idxs) > 1: # 여러개면 우선순위 정해서 어디로갈지 정해야함
        for i in range(1, len(min_idxs)):
            if min_santa[1] < santas[min_idxs[i]][1]:
                min_santa = santas[min_idxs[i]]
            elif min_santa[1] == santas[min_idxs[i]][1]:
                if min_santa[2] < santas[min_idxs[i]][2]:
                    min_santa = santas[min_idxs[i]]
    
    min_go_idx = 0 # 루돌프 이동
    min_go = float("inf") 
    for i in range(8):
        nR = [R[0]+go[i][0], R[1]+go[i][1]]
        if min_go > Dist(nR, min_santa[1:3]):
            min_go = Dist(nR, min_santa[1:3])
            min_go_idx = i
    
    nR = [R[0]+go[min_go_idx][0], R[1]+go[min_go_idx][1]] # 루돌프 한번 이동했음
    return nR, min_go_idx

def SGO():
    global N, santas, n, R
    #산타 움직임
    #1번부터 P번까지 순서대로 움직임
    for i in range(n):
        if santas[i][4] == 1: # 기절이면 이번 턴 넘김
            santas[i][4] = 2
            continue
        elif santas[i][4] == -1: # 탈락이라 넘김
            continue
        elif santas[i][4] == 2: # 기절이면 초기화
            santas[i][4] = 0
        else: # 움직이자
            d = Dist(R, santas[i][1:3]) # 거리 구하고
            min_go_idx = 0
            min_go = float("inf")
            for j in range(4): #루돌프에게 가까워지는 방향구하기
                nS = [santas[i][1]+go[j][0], santas[i][2]+go[j][1]]
                nd = Dist(nS, R)
                if nd > d: # 더 멀어지는경우
                    continue
                
                flag = 0
                for s in range(n):
                    if nS == santas[s][1:3]: # 산타가 있음
                        flag = 1
                if flag == 1: # 산타가 있어서 여기로 이동 불가
                    continue

                if min_go > nd: # 루돌프와 가까워지는 곳이 있다면
                    min_go = nd
                    min_go_idx = j
            
            if min_go == float("inf"): # 산타가 못 움직이는 경우
                continue
            else:
                #루돌프에게 가까워지는 방향으로 1칸 이동
                santas[i][1] += go[min_go_idx][0]
                santas[i][2] += go[min_go_idx][1]
            if santas[i][1:3] == R: # 산타-루돌프 충돌 일어남
                collapse("S", i, min_go_idx)
    return

def check_R(): # 루돌프 충돌 확인 유무
    global R, santas, n
    for i in range(n):
        if santas[i][1:3] == R:
            return i
    return -1

def check_S(i, d): # 산타끼리 부딪히는지 확인
    global santas, go, n, out
    for j in range(n):
        if i == j:
            continue
        
        if santas[i][1:3] == santas[j][1:3]: # 부딪혔노 ㅋㅋ 상호작용 해야겠지?
            santas[j][1] -= go[d][0] # 1칸씩 밀려남
            santas[j][2] -= go[d][1]
            if santas[j][1] > N or santas[j][2] > N: # 나가면 탈락
                santas[j][4] = -1
                out += 1
            else:
                check_S(j, d)
            return
    return

def collapse(opt, i, d): # i번째 산타랑 부딪힘. 방향 d
    global N, R, santas, C, D, go, out
    if opt == "R": #루돌프 이동해서 산타-루돌프 충돌
        #print("HERE Collapse")
        santas[i][3] += C #일어나면 점수 얻기 산타 +C
        #산타가 루돌프가 이동해온 방향으로 C칸만큼 밀려남 + 기절함(다음턴 움직X),
        santas[i][1] += go[d][0]*C; santas[i][2] += go[d][1]*C; santas[i][4] = 1 

        if santas[i][1] > N or santas[i][2] > N: #   밀려난 곳이 게임 밖이면 탈락
            santas[i][4] = -1
            out += 1
            return
        check_S(i, d) #밀려난 곳에 산타가 있는지 없는지 확인 후 상호작용      
    else: #산타 이동해서 산타-루돌프 충돌
        santas[i][3] += D #일어나면 점수 얻기 산타 +D
        #산타가 이동해온 반대 방향으로 D 칸 밀려남 + 기절함(다음턴 움직X), 기절시 움직X
        santas[i][1] -= go[d][0]*D; santas[i][2] -= go[d][1]*D; santas[i][4] = 1

        if santas[i][1] > N or santas[i][2] > N: #   밀려난 곳이 게임 밖이면 탈락
            santas[i][4] = -1
            out += 1
            return
        check_S(i, d) #밀려난 곳에 산타가 있는지 없는지 확인 후 상호작용    
    return

for m in range(M): # M번 턴
    #print("=================================")
    if n == out: # 모든 산타가 탈락하면 끝
        break
    #print(R)
    #for i in range(n):
    #    print(santas[i][1:3], santas[i][4])

    #루돌프 움직임 
    #산타향해 1칸 돌진. 기절한애도 됨. go에서 8방향
    #가장 가까운 산타가 2명이상이라면 sort(reverse=True)로 결정(r이 클수록, c가 클수록)
    R, d = RGo(R) # 루돌프 움직인 방향 d
    #산타-루돌프 충돌일어나나?
    p = check_R()
    #print(m, " : ", p)
    if p == -1:
        pass
    else: # p번째 산타-루돌프 충돌일어남. 방향 d
        #print("HERE Collapse")
        collapse("R", p, d) # 상호작용까지 딱
    
    SGO() #산타 움직임

    #print("++++++++++++++++++++++++++++++++++")
    #print(R)
    for i in range(n): #매턴 이후에 탈락하지 않은 산타들에게 1점씩 추가로 부여
        if santas[i][4] != -1:
            santas[i][3] += 1
        #print(santas[i][1:])
    #print("=================================")
    
for i in range(n):
    print(santas[i][3], end=" ")
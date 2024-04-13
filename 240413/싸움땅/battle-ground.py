import heapq as hq

class person:
    def __init__(self, idx, r,c, d, power, gun=0, score=0):
        self.idx = idx
        self.r = r
        self.c = c
        self.power = power
        self.gun = gun
        self.d = d
        self.score = score
    
    def changeGun(self, g):
        self.gun = g
    
    def getScore(self, s): 
        self.score += s

    def __lt__(self, other):
        if self.power + self.gun != other.power + other.gun:
            return self.power + self.gun < other.power + other.gun
        return self.power < other.power

n, m, k = map(int, input().split()) # n*n, m 명, k 라운드
board = {} #(r,c):[guns]
board[0,0] = []
for i in range(1, n+1):
    board[0,i] = []
    line = list(map(int, input().split()))
    for j in range(1, n+1):
        if line[j-1] == 0:
            board[i,j] = []
            continue
        board[i,j] = [-line[j-1]]
    board[i,0] = []

person_location = [[0]*(n+1) for _ in range(n+1)]
direction = [[-1,0], [0,1], [1,0], [0,-1]]
people = {}
for i in range(1, m+1):
    line = list(map(int, input().split()))
    people[i] = person(i, line[0], line[1], line[2], line[3])
    person_location[line[0]][line[1]] = i

def Move_loser(p):
    global n, direction, board, person_location
    #print("move loser")
    r,c,d = p.r, p.c, p.d
    cnt = 0
    #print("r,c,d : ", r, c, direction[d])
    while True:
        go = direction[d]
        nr, nc = r+go[0], c+go[1]
        if nr <= 0 or nc <=0 or nr >= n+1 or nc >=n+1 or person_location[nr][nc] != 0:
            d = (d+1)%4
            cnt+=1
            continue
        #print("nr, nc, d : ", nr, nc, direction[d])
        if cnt == 4: #갈 데가 없음. 근데 아마 있을거임
            return
        person_location[nr][nc] = p.idx #person location 채우기
        p.r, p.c, p.d = nr, nc, d #person 정보 변경
        if board[nr, nc] == []: # board에 총이 없음
            pass
        else: # board에 총이 있음
            gun_power = -board[nr, nc][0] # 필드에 있는 총 중에 젤 센거
            if p.gun >= gun_power: # 갖고 있는 총이 더 셈
                pass
            else: # 필드에 있는 총이 더 셈
                gun = -hq.heappop(board[nr, nc]) # 필드에 있는 총
                if p.gun > 0: # 가진 총이 있으면
                    hq.heappush(board[nr, nr], -p.gun) # 총 board에 내려놓기
                p.changeGun(gun) # 총바꿔!
        return
    return

def Fight(A, B):
    # A랑 B랑 싸움. (둘다 idx)
    # B가 있는 장소에서 싸웠음 ㅠ
    global people, person_location, board
    A = people[A]
    B = people[B]
    #print("A info(idx, r, c, d) : ", A.idx, A.r, A.c, direction[A.d])
    #print("B info(idx, r, c, d) : ", B.idx, B.r, B.c, direction[B.d])
    now_r, now_c = B.r, B.c; person_location[now_r][now_c] = 0
    winner = B; loser = A;
    if A > B: # A가 이겼음
        winner = A; loser = B
    #print("winner idx r c d : ", winner.idx, winner.r, winner.c, winner.d)
    #print("loser idx r c d : ", loser.idx, loser.r, loser.c, loser.d)
    score = winner.power + winner.gun - (loser.power + loser.gun)
    winner.getScore(score) # 점수 획득
    
    loser_gun = loser.gun
    #print("loser info(idx power) : ", loser.idx, loser.gun)
    if loser_gun != 0:
        loser.gun = 0 #진 사람은 총을 내려둠
        hq.heappush(board[now_r, now_c], -loser_gun) # board에 총을 내려둠
    
    #print("winner info(idx, r, c, d, power, gun)", winner.idx, winner.r, winner.c, winner.d, winner.power, winner.d)
    if board[now_r, now_c] != []:
        powerful_gun = -board[now_r, now_c][0] # 격자에서 젤 센 총
        #print("board info(guns) : ", board[now_r, now_c])
        if powerful_gun > winner.gun: # 승자는 격자에 있는 총 중에 젤 좋은거로 바꿔 갈아치움
            #print("change gun : ", winner.gun, powerful_gun)
            hq.heappush(board[now_r, now_c], -winner.gun)
            winner.changeGun(-hq.heappop(board[now_r, now_c]))
            #print("board info(guns) : ", board[now_r, now_c])
    #print("after winner info(idx, power, gun)", winner.idx, winner.power, winner.gun)
    person_location[now_r][now_c] = winner.idx # 이긴 사람으로 board 갱신
    
    Move_loser(loser) # 진 사람 이동
    #print("after winner loser info")
    #print("winner idx r c d : ", winner.idx, winner.r, winner.c, winner.d)
    #print("loser idx r c d : ", loser.idx, loser.r, loser.c, loser.d)
    return

def Move_person(p, lose=0):
    global n, direction, person_location
    r,c,d = p.r, p.c, p.d
    person_location[r][c] = 0
    go = direction[d]
    #print("r, c : ", r, c, direction[d])
    nr, nc = r+go[0], c+go[1]
    if nr <= 0 or nc <=0 or nr >= n+1 or nc >=n+1:  # 격자 밖으로 나감
        d = (d+2)%4 # 방향 바꾸기
        go = direction[d]
        nr, nc = r+go[0], c+go[1] #nr,nc 갱신
    
    p.r = nr; p.c = nc; p.d = d # person r,c,d 갱신
    #print("idx nr, nc : " , p.idx, p.r, p.c)
    
    if person_location[nr][nc] != 0: # 사람이 있음. 싸워야지 반드시 싸워야지
        #print("lets Fight")
        #print("fight idx nr, nc : " , p.idx, p.r, p.c)
        Fight(p.idx, person_location[nr][nc])
        #pass
    else: # 사람이 없음
        if board[nr, nc] == []: # board에 총이 없음
            pass
        else: # board에 총이 있음
            gun_power = -board[nr, nc][0] # 필드에 있는 총 중에 젤 센거
            if p.gun >= gun_power: # 갖고 있는 총이 더 셈
                pass
            else: # 필드에 있는 총이 더 셈
                gun = -hq.heappop(board[nr, nc]) # 필드에 있는 총
                if p.gun > 0: # 가진 총이 있으면
                    #print("put down gun(idx gun) : ", p.idx, p.gun)
                    hq.heappush(board[nr, nc], -p.gun) # 총 board에 내려놓기
                p.changeGun(gun) # 총바꿔!
        person_location[nr][nc] = p.idx
    return

def Round1():
    global m, people
    for i in range(1, m+1):
        Move_person(people[i])
    # 싸우게되면
    #Fight()
    return

stop = -1
for i in range(1, k+1):
    Round1()
    if i == stop:
        print("board : ")
        for s in range(1, n+1):
            for t in range(1, n+1):
                print(board[s, t], end= " ")
            print()
        #for k, v in people.items():
        #    print(k, " person(r,c, d, power, gun score) : ", v.r, v.c, v.d, v.power, v.gun, v.score)
        #print("person location(visualization) : ")
        for j in range(1,n+1):
            print(person_location[j][1:])
        break

for k, v in people.items():
    print(v.score, end=" ")
#print(board)
#print(people)
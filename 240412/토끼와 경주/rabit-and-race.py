# 100 N M P pid_1 d_1 pid_2 d_2 ... pid_p d_p
# 200 K S
# 300 pid_t L
# 400 
import heapq as hq

class Rabbit:
    def __init__(self, r,c,pid, d, cnt=0, score=0):
        self.cnt = cnt
        self.r = r
        self.c = c
        self.pid = pid
        self.d = d
        self.score = score
    
    def __lt__(self, other):
        if self.cnt != other.cnt:
            return self.cnt < other.cnt
        if self.r + self.c != other.r + other.c:
            return self.r + self.c < other.r + other.c
        if self.r != other.r:
            return self.r < other.r
        if self.c != other.c:
            return self.c < other.c
        return self.pid < other.pid
    
    def getScore(self, S):
        self.score += S

N, M, P = 0, 0, 0
Rabbits = {} # pid:(r,c, pid, d, cnt, score)

def init(q):
    global N, M, P

    N, M, P = q[1], q[2], q[3]
    for i in range(P):
        pid = q[2*i + 4]
        d = q[2*i + 5]
        Rabbits[pid] = Rabbit(1,1, pid, d, 0) #(r,c, pid, d, cnt, score)

def go(next_, N):
    next_ = next_%(2*N-2)
    
    if next_ >= N:
       next_ = 2*N - next_
    if next_ == 0:
        next_ = 2
    return next_
def Rule2(q):
    global N, M, P, Rabbits
    K, S = q[1], q[2]

    rabbit_q = []
    for k, v in Rabbits.items():
        hq.heappush(rabbit_q, v)
    
    total_score = 0
    jumps_ = set()
    for _ in range(K):
        # 우선순위가 가장 높은 토끼
        go_rabbit = hq.heappop(rabbit_q)

        r,c, d = go_rabbit.r, go_rabbit.c, go_rabbit.d
        UP = [-(go(r-d, N)+c), -go(r-d, N), -c] # 행 r N
        DOWN = [-(go(r+d, N)+c),-go(r+d, N), -c]
        LEFT = [-(r+go(c-d, M)), -r, -go(c-d, M)]
        RIGHT = [-(r+go(c+d, M)), -r, -go(c+d, M)]

        All_mov = []
        hq.heappush(All_mov, UP)
        hq.heappush(All_mov, DOWN)
        hq.heappush(All_mov, LEFT)
        hq.heappush(All_mov, RIGHT)
        next_mov = hq.heappop(All_mov)[1:]
        next_mov[0] *= -1; next_mov[1] *= -1;
        score = sum(next_mov)

        go_rabbit.r = next_mov[0] # go_rabbit r 업데이트
        go_rabbit.c = next_mov[1] # c 업데이트
        go_rabbit.cnt += 1 # 점프 1회
        jumps_.add(go_rabbit.pid) # 점프한 토끼 pid 추가
        hq.heappush(rabbit_q, go_rabbit) # 다시 넣어줘잇!
        
        Rabbits[go_rabbit.pid].getScore(-score) # 점프한애만 빼고 나머지는 다 score 더 해줘야함
        Rabbits[go_rabbit.pid].r = next_mov[0] # Rabbits r 업데이트
        Rabbits[go_rabbit.pid].c = next_mov[1] # Rabbits c 업데이트
        total_score += score # 나중에 다 줘야함
    
    for k, v in Rabbits.items(): # 모든애들 다 줌. 점프한애들은 빼놔서 다 주면 됨
        v.getScore(total_score)
    
    bonus_rabbits = []
    for pid in jumps_:
        gone_rab = Rabbits[pid]
        hq.heappush(bonus_rabbits, [-(gone_rab.r+gone_rab.c), -gone_rab.r, -gone_rab.c, -pid])
    bonus_rabbit_pid = -bonus_rabbits[0][3]
    Rabbits[bonus_rabbit_pid].getScore(S)

    return

def Rule3(q):
    global Rabbits
    pid, L = q[1], q[2]
    Rabbits[pid].d *= L
    return

def Rule4(q):
    global Rabbits
    max_score = 0
    for k, v in Rabbits.items():
        max_score = max(max_score, v.score)
    print(max_score)
    return

Q = int(input())
stop = -1
for i in range(Q):
    q = list(map(int, input().split()))
    if q[0] == 100:
        init(q)
    elif q[0] == 200:
        Rule2(q)
    elif q[0] == 300:
        Rule3(q)
    elif q[0] == 400:
        Rule4(q)

    if i == stop:
        print("======== Rabbits ======== ")
        for k, v in Rabbits.items():
            print(k, "(r,c,d,cnt,score) : ", v.r, v.c, v.d, v.cnt, v.score)
        break
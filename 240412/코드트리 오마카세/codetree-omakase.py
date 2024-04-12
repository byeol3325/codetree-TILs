L, Q = map(int, input().split()) # 초밥의 벨트 길이 L, 명령 수 Q

# {위치 : 사람} person:name, n
# {스시 사람이름: 위치}
seats = {} # 위치:사람-(name, n)
sushi_belt = {} # 스시 사람 이름 : 위치

class person:
    def __init__(self, name, n):
        self.name = name
        self.n = n
    
    def eat(self):
        self.n -= 1

def eat():
    global L, seats, sushi_belt
    if len(seats) == 0:
        return

    for k, v in sushi_belt.items(): # {스시 사람이름: 위치}
        res = []
        for i in range(len(v)): # 
            if v[i] in seats: # 자리에 사람이 앉아 있긴함
                if seats[v[i]].name == k: # 해당자리에 사람이 있음
                    seats[v[i]].eat()
                    #print("now eat!!!!")
                    if seats[v[i]].n == 0: # 다 먹어서 떠남 ㅠ
                        del seats[v[i]]
                    continue
                else: # 다른 사람이라 다시 올려잇!
                    #print("other person")
                    res.append(v[i])
            else: # 사람이 안 앉아 있음
                #print("no person ")
                res.append(v[i])   
        sushi_belt[k] = res
    return

def Rotate(gap):
    global L, seats, sushi_belt
    for _ in range(gap):
        for k, v in sushi_belt.items():
            for i in range(len(v)):
                v[i] += 1
                if v[i] >= L:
                    v[i] -= L
        eat()
    return


def Rule1(q): # 100 t x name
    global sushi_belt # 스시 사람 이름 : 위치
    x = int(q[2]); name = q[3]
    if name not in sushi_belt:
        sushi_belt[name] = [x]
    else:
        sushi_belt[name].append(x)
    return

def Rule2(q): # 200 t x name n
    global seats
    x = int(q[2]); name = q[3]; n = int(q[4])
    seats[x] = person(name, n) # x좌석에 사람 앉힘. n개 쳐먹을 예정
    return

def Rule3(q): # 300 t
    global seats, sushi_belt
    p_num = len(seats); s_num = 0
    
    for k, v in sushi_belt.items(): # 스시 사람 이름 : 위치
        s_num += len(v)
    print(p_num, s_num)
    return



#seats = {} # 위치:사람-(name, n)
#sushi_belt = {} # 스시 사람 이름 : 위치
# ==========================================

pri_t = 0 # rotate 시키기 위한 이전 시간 트래킹
stop = -1
for k in range(1, Q+1):
    q = input().split()
    rule = int(q[0]) # 100, 200, 300 명령어
    t = int(q[1]) # 시간
    
    # 모든 rule은 회전하고 시작임.
    Rotate(t-pri_t) # 시간 차만큼 돌려돌려

    if rule == 100: # 100 t x name
        Rule1(q); eat()
    elif rule == 200: # 200 t x name n
        Rule2(q); eat()
    else: # 300 t
        Rule3(q)
    
    pri_t = t # rotate 시키기 위한 이전 시간 트래킹
    
    if k == stop:
        print("TURN : ", k)
        print("SEATS : ")
        for k, v in seats.items():
            print(k, v)
        print("sushi_belt : ")
        for k, v in sushi_belt.items():
            print(k, v)
        break
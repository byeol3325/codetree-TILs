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


# {위치 : 사람 이름} person:name, n
# {사람 : 먹는 수}
# {사람 : 위치}
# {스시 사람이름: 위치}
def eat(gap=0):
    global L, seats, sushi_belt
    if not seats: #없으면 넘겨
        for k, v in sushi_belt.items():
            for i in range(len(v)):
                sushi_belt[k][i] = (sushi_belt[k][i]+gap)%L
        return

    for k, v in sushi_belt.items(): # {스시 사람이름: 위치}
        res = []
        for i in range(len(v)): #
            locations = seats.copy().keys()
            eat_ = 0
            if v[i]+gap >= L:
                for loc in locations:
                    if v[i] <= loc or loc <= (v[i]+gap)%L: # 위치에 한번 들림
                        if seats[loc].name == k:
                            seats[loc].eat()
                            #print("eat k : ", k)
                            if seats[loc].n == 0:
                                del seats[loc]
                            eat_ = 1
                            break
                        else:
                            continue
                            #res.append((v[i]+gap)%L)
                    else:
                        continue
                        #res.append((v[i]+gap)%L)
            else: # v[i]+gap 이 L보다 작은 경우
                for loc in locations: # 위치 : 사람
                    if v[i] <= loc <= v[i]+gap: # 위치에 한번 들림
                        if seats[loc].name == k: # 이름이 같으면 먹어야지
                            seats[loc].eat()
                            #print("eat k : ", k)
                            if seats[loc].n == 0:
                                del seats[loc]
                            eat_ = 1
                            break
                        else: #이름이 없음
                            continue
                            #res.append(v[i]+gap)
                    else: # 위치에 들리지 않음
                        continue
            if eat_ == 0:
                res.append((v[i]+gap)%L)
        sushi_belt[k] = res
    return

def Rotate(gap):
    global L, seats, sushi_belt
    eat(gap)
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
    gap = t-pri_t
    Rotate(gap) # 시간 차만큼 돌려돌려

    if rule == 100: # 100 t x name
        Rule1(q); eat()
    elif rule == 200: # 200 t x name n
        Rule2(q); eat()
    else: # 300 t
        Rule3(q)
    
    pri_t = t # rotate 시키기 위한 이전 시간 트래킹
    
    if k == stop:
        print("TURN time : ", k, t)
        print("SEATS : ")
        for k, v in seats.items():
            print(k, v.name, v.n)
        print("sushi_belt : ")
        for k, v in sushi_belt.items():
            print(k, v)
        break
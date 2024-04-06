import sys
input = sys.stdin.readline

L, Q = map(int, input().split()) # 초밥의 벨트 길이 L, 명령 수 Q
sushi_belt = [[] for _ in range(L)] # 벨트
people = [[] for _ in range(L)] # 사람 자리

def eat():
    global L, sushi_belt, people
    for i in range(L):
        person = people[i]
        cnt = 0 # 몇개 쳐먹노 임마!
        res = []
        if len(person) != 0: # 누군가 앉아있음. 1명까지만 앉아있음
            for j in range(len(sushi_belt[i])):
                if person[0] == sushi_belt[i][j]: # 이름 같은거. 먹어버릴거임 ㅅㄱ
                    cnt += 1
                else: # 못 먹으니 다시 그릇 내려놔
                    res.append(sushi_belt[i][j])
            sushi_belt[i] = res # 못 먹은거 다시 올리기
            people[i][1] -= cnt # 먹은 수 빼기
            
            if people[i][1] == 0: # 다 먹었으면 사람 일어나 이새끼야!
                people[i] = []         
    return

def Rotate(gap):
    global L, sushi_belt

    for i in range(gap): # 하나씩 회전시키기
        result = []; result.append(sushi_belt[L-1]) # 맨뒤는 앞으로
        for j in range(L-1): # 나머지 붙이기
            result.append(sushi_belt[j])
        
        sushi_belt = result # 회전시키기!
    eat() # 먹기!
    #print("========================================")
    #print(sushi_belt)
    #print(people)
    #print("========================================")
    return 

def Rule1(q): # 100 t x name
    global sushi_belt
    x = int(q[2]); name = q[3]

    cnt = 0; res = []
    if people[x] != []: # 사람이 앉아있고 그대로 같은 이름이면 바로 쳐먹기
        if name == people[x][0]: # 이름 있음 ㅈ댐 ㅋㅋ
            cnt += 1
            people[x][1] -= cnt
            if people[x][1] == 0: # 다 먹었으면 비우기
                people[x] = [] 
        else: # 없음
            sushi_belt[x].append(name) # 없으면 올리기
    else:
        sushi_belt[x].append(name)
    
    return

def Rule2(q): # 200 t x name n
    global sushi_belt, people
    x = int(q[2]); name = q[3]; n = int(q[4])
    people[x] = [name, n] # x좌석에 사람 앉힘. n개 쳐먹음
    
    # 앉은 즉시 있으면 바로 쳐먹기
    cnt = 0; res = [] # 숫자세기, 이름 다른 나머지
    for j in range(len(sushi_belt[x])):
        if name == sushi_belt[x][j]: # 이름 같으면 바로 먹기
            cnt += 1
        else:
            res.append(sushi_belt[x][j])
    people[x][1] -= cnt # 먹은 수 빼기
    sushi_belt[x] = res # 먹은거 빼기
    if people[x][1] == 0: # 다 먹었으면 비우기
        people[x] = [] 
    #print("========================================")
    #print(sushi_belt)
    #print(people)
    #print("========================================")
    return

def Rule3(q): # 300 t
    global L, sushi_belt, people
    s_num = 0; p_num = 0
    #print("========================================")
    #print(sushi_belt)
    #print(people)
    #print("========================================")
    for i in range(L): # 사람수, 스시 수 세기
        s_num += len(sushi_belt[i])
        if people[i] != []:
            p_num += 1
    print(p_num, s_num)

    return


pri_t = 0 # rotate 시키기 위한 이전 시간 트래킹
for _ in range(Q):
    q = input().split()
    rule = int(q[0]) # 100, 200, 300 명령어
    t = int(q[1]) # 시간
    
    # 모든 rule은 회전하고 시작임.
    Rotate(t-pri_t) # 시간 차만큼 돌려돌려

    if rule == 100: # 100 t x name
        Rule1(q)
    elif rule == 200: # 200 t x name n
        Rule2(q)
    else: # 300 t
        Rule3(q)
    
    pri_t = t # rotate 시키기 위한 이전 시간 트래킹
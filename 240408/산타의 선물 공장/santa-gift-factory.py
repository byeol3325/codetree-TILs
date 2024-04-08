# m개 벨트. 벨트 위에 n/m개 물건들 놓아 총 n개 물건 준비
# 각 물건에는 고유한 번호ID와 무게W가 적혀있음
# 번호는 무조건 다르고 무게는 같을 수 있음

# 물건하차
# 산타가 원하는 상자의 최대 무게인 w_max. 
# 1번부터 m번까지 벨트 보면서 "맨 앞"에 있는 선물 중 선물 무게가 w_max이하면 하차. 그렇지 않으면 맨 뒤로
# 벨트에 있던 상자가 빠지면 한칸씩 내려와야함
# 1회 움직. 내려온 상자들 무게 총합

# 물건 제거 r_id
# 제거하기 위한 물건 고유번호 r_id. 상자가 놓여져있는 벨트에서 상자 제거. 뒤에 있던 상자들은 앞으로 한칸씩
# 그러한 상자가 있으면 r_id, 없으면 -1 출력

# 물건 확인. f_id
# 해당 상자 위에 있는 모든 상자를 앞으로 가져옴
# 없으면 -1 있으면 벨트 번호 출력()

# 벨트 고장. b_num
# b_num 벨트 고장. 다시 사용X. 
# 모든 벨트가 망가지는 경우 없음
# 1 2 3 4 5 ... m 1 2 .. 순서로 탐색. 그대로 옮기기
# b_num이 이미 망가져있으면 -1, 아니면 b_num 출력

Q = int(input())
# 100 n m ID1 ID2 ... IDn W1 W2 ... Wn //  3 + n + n 
settings = list(map(int, input().split()))
n, m = settings[1], settings[2]

# 아이템들 벨트 정리
belts = [[] for _ in range(m+1)]; #print(belts)
weights = {}
for i in range(n):
    ID = settings[i+3]
    W = settings[i+3+n]
    idx = i//(n//m) + 1
    #print(i, idx)
    belts[idx].append(ID)
    weights[ID] = W
#print(belts[1:])

on = [1] * (m+1) # 고장나면 0
head = [0] * (m+1)
tail = [0] * (m+1)
nums = [n//m] * (m+1)
#print(head)
before = {}
after = {}

for i in range(1, m+1):
    num_item = len(belts[i])
    head[i] = belts[i][0]
    tail[i] = belts[i][-1]
    for j in range(num_item):
        #print(belts[i][j])
        item = belts[i][j]
        #print(item)
        if j == 0: # 맨 앞은 after만 있음
            after[item] = belts[i][j+1]
            before[item] = 0
        elif j == num_item-1: # 맨 뒤는 before만 있음
            after[item] = 0
            before[item] = belts[i][j-1]
        else:
            after[item] = belts[i][j+1] # 뒤
            before[item] = belts[i][j-1] # 앞 

def Head_to_Tail(i, w):
    # 올리면 0, 반환시 무게
    head_ = head[i]; tail_ = tail[i]; next_ = after[head_]
    result = 0

    if weights[head_] <= w: # 무게 이하면 빼기
        result += weights[head_]
        weights[head_] = -1 # 이제 없음
        before[next_] = 0
        head[i] = next_ # head 바꿔주기
        nums[i] -= 1 # 수 하나 빼기
    else: # 아니면 올리기
        before[next_] = before[head_] # next_의 앞에는 이전 대가리 앞
        before[head_] = tail_ # head_는 올라가니까 이전 tail_이 됨
        after[head_] = 0 # head_는 올라가서 after이 0
        after[tail_] = head_ # 이전 tail_의 after는 새로운 head

        head[i] = next_
        tail[i] = head_
    
    return result

def Rule2(q): # 200 w_max
    w_max = q[1]
    total = 0
    for i in range(1, m+1):
        if nums[i] == 0: # 없으면 다음 벨트
            continue
        total += Head_to_Tail(i, w_max)
    print(total)
    return

# 물건하차
# 산타가 원하는 상자의 최대 무게인 w_max. 
# 1번부터 m번까지 벨트 보면서 "맨 앞"에 있는 선물 중 선물 무게가 w_max이하면 하차. 그렇지 않으면 맨 뒤로
# 벨트에 있던 상자가 빠지면 한칸씩 내려와야함
# 1회 움직. 내려온 상자들 무게 총합
def Rule3(q): # 300 r_id
    r_id = q[1]
    if r_id not in weights or weights[r_id] == -1: # r_id가 없는 경우
        print(-1)
        return
    
    for i in range(1, m+1):
        if if_inBelt_remove(i, r_id):
            break
    print(r_id)
    return

def if_inBelt_remove(i, r_id):
    if nums[i] == 0:
        return False

    now = head[i] # 초깃값
    for _ in range(nums[i]):
        if now == r_id:
            head[i] = before[now] # head 바꾸기 head[2] = 19
            # before[now],  before[19] = 0 after[19] = 25
            after[before[now]] = after[now]
            # after[now], before[25] = 19 after[25] = 0
            before[after[now]] = before[now] # now의 after이 after의 before가 됨
            weights[now] = -1 # 제거
            nums[i] -= 1 # 수 줄이기
            return True
        if now == 0: # 끝남
            return False
        else:
            now = after[now] # 다음꺼 탐색
    return False

def Rule4(q): # 400 f_id
    f_id = q[1]
    if f_id not in weights or weights[f_id] == -1: # f_id가 없는 경우
        print(-1)
        return
    
    for i in range(1, m+1):
        for _ in range(nums[i]):
            Head_to_Tail(i, 0) # 순서 바꾸고
            if head[i] == f_id:
                print(i)
                return
    return

def Rule5(q): # 500 b_num
    b_num = q[1]
    if on[b_num] == 0: # 이미 망가져있음
        print(-1)
        return
    on[b_num] = 0 # 망가뜨리고
    t = -1 # 넘길곳 찾기
    for i in range(m):
        # m == 3
        if on[(b_num+i)%m + 1] == 1:# 고장 X
            t = (b_num+i)%m + 1
            break
    
    s_head = head[b_num]; s_tail = tail[b_num]; head[b_num] = 0; tail[b_num] = 0
    t_head = head[t]; t_tail = tail[t]
    # t //// s 
    tail[t] = s_tail
    if t_head == 0:
        head[t] = s_head
        #before[s_head] = s_tail
    
    after[t_tail] = s_head
    before[s_head] = t_tail

    nums[t] += nums[b_num]
    nums[b_num] = 0
    print(b_num)
    return


"""
print("NUMS : ", nums[1:])
print("HEAD : ", head[1:])
print("TAIL : ", tail[1:])
print("BEFORE : ", before)
print("AFTER : ", after)
print("WEIGHTS : ", weights)
"""
stop = -1
for i in range(1, Q):
    q = list(map(int, input().split()))
    if i == stop:
        print("TIME : ", i, ", ", q)
    
    if q[0] == 200: # 200 w_max
        Rule2(q)
    elif q[0] == 300: # 300 r_id
        Rule3(q)
    elif q[0] == 400: # 400 f_id
        Rule4(q)
    elif q[0] == 500: # 500 b_num
        Rule5(q)
    
    if i == stop:
        print("NUMS : ", nums[1:])
        print("HEAD : ", head[1:])
        print("TAIL : ", tail[1:])
        print("BEFORE : ", before)
        print("AFTER : ", after)
        print("WEIGHTS : ", weights)
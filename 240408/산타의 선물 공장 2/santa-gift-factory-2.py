q = int(input())
  
n, m = -1, -1  # n개의 벨트, m개의 물건 
prev, next = [0] * 100001, [0] * 100001   # id에 해당하는 상자의 prev, next값
head, tail, num = [0] * 100001, [0] * 100001, [0] * 100001  # 각 벨트 별 head id, tail id, 선물 수 

# 1) 공장 설립
def build(order):
    n, m = order[1], order[2]   
    belt = [[] for i in range(n)]

    for i in range(1, m+1):
        belt[order[i+2]-1].append(i)

    for i in range(n):
        if len(belt[i]) == 0:
            continue

        head[i] = belt[i][0]
        tail[i] = belt[i][-1]
        num[i] = len(belt[i])

        for j in range(len(belt[i])-1):
            next[belt[i][j]] = belt[i][j+1]
            prev[belt[i][j+1]] = belt[i][j]


# 2) 물건 모두 옮기기
def move(order):
    src, dst = order[1] - 1, order[2] - 1

    # src에 물건이 없다면 그대로 dst내 물건 수가 답이 됨 
    if num[src] == 0:
        print(num[dst])
        return
    
    # dst에 물건이 없다면 그대로 옮겨줌 
    elif num[dst] == 0:
        head[dst] = head[src]
        tail[dst] = tail[src]

    else:
        dh = head[dst]
        head[dst] = head[src]
        st = tail[src]
        next[st] = dh
        prev[dh] = st
        
    head[src], tail[src] = 0, 0
    num[dst] += num[src]
    num[src] = 0

    print(num[dst])


# 해당 벨트의 head를 제거함 
def remove(idx):
    # 해당 벨트가 비어있을 경우 불가능함 -> 0 리턴 -> 뒤의 push 함수에서 이어짐 
    if num[idx] == 0:
        return 0

    # 해당 벨트 내 선물 개수가 1개라면 -> head, tail 전부 삭제 
    if num[idx] == 1:
        hid = head[idx]
        head[idx], tail[idx] = 0, 0
        num[idx] = 0
        return hid

    hid = head[idx]   # 제거될 head값 
    nh = next[hid]   # 바뀐 head값 
    next[hid], prev[nh] = 0, 0
    num[idx] -= 1
    head[idx] = nh

    return hid


# 해당 벨트에 head를 추가함 
def push(idx, nh):
    # 불가능할 경우 진행하지 않음 
    if nh == 0:
        return 

    # 해당 벨트가 비어있을 경우 -> head, tail이 동시에 추가됨
    if num[idx] == 0:
        head[idx], tail[idx] = nh, nh
        num[idx] = 1

    else:
        hid = head[idx]   # 원래의 head값 -> 추가한 뒤에는 nh-hid순이 됨 
        next[nh] = hid
        prev[hid] = nh
        head[idx] = nh
        num[idx] += 1


# 3) 앞 물건만 교체하기
def change(order):
    src, dst = order[1] - 1, order[2] - 1

    sh = remove(src)
    dh = remove(dst)
    push(dst, sh)
    push(src, dh)

    print(num[dst])


# 4) 물건 나누기 
def divide(order):
    src, dst = order[1] - 1, order[2] - 1

    cnt = num[src]
    bid = []

    # src에서 cnt//2개만큼 선물들을 빼줌 
    for _ in range(cnt//2):
        bid.append(remove(src))

    # 거꾸로 뒤집어서 하나씩 dst에 선물들을 넣어줌
    for i in range(len(bid)-1, -1, -1):
        push(dst, bid[i])

    print(num[dst])


# 5) 선물 정보 얻기 
def gift(order):
    pnum = order[1]

    if prev[pnum] != 0:
        a = prev[pnum]
    else:
        a = -1

    if next[pnum] != 0:
        b = next[pnum]
    else:
        b = -1

    print(a + 2 * b)


# 6) 벨트 정보 얻기
def belt(order):
    bnum = order[1] - 1

    if head[bnum] != 0:
        a = head[bnum]
    else:
        a = -1

    if tail[bnum] != 0:
        b = tail[bnum]
    else:
        b = -1

    c = num[bnum]
    print(a + 2 * b + 3 * c)
        
           
for _ in range(q):
    order = list(map(int, input().split()))

    if order[0] == 100:
        build(order)            
    elif order[0] == 200:
        move(order)
    elif order[0] == 300:
        change(order)
    elif order[0] == 400:
        divide(order)
    elif order[0] == 500:
        gift(order)
    else:
        belt(order)
# 선물 공장. 산타가 각 벨트의 정보와 선물의 정보를 조회하는 기능

# 1. n개 벨트 섩치, m개 물건 준비.
#    m 개 선물의 위치가 공백을 두고 지어짐. 각 선물의 번호는 오름차순으로. (1,5) (2,3,4) ...

# 2. 물건 모두 옮기기 (m_src) => (m_dst)  ///  print(m_dst)
#    m_src 벨트 선물은 모두 m_dst 벨트 선물들로 옮김. 
#    m_src 없으면 안 옮겨도 됨. 옮긴 뒤에 m_dst 벨트에 잇는 선물들 개수 출력.
#    오름차순 그대로 유지

# 3. 앞 물건만 교체 (m_src) <=> (m_dst)  ///  print(m_dst)
#    mm_src 벨트에 있는 선물 중 가장 앞에 있는 선물을 m_dst 벨트 선물들 중 가장 앞에 있는 선물과 교체
#   없으면 있는 곳에서만 옮기기 
#    옮긴 뒤에 m_dst벨트에 있는 선물 갯수 출력

# 4. 물건 나누기 (m_src) => (m_dst)    print(m_dst)
#    m_src 번째 벨트에 있는 선물 갯수 n이라고 할 때 가장 앞에앞에서 floor(n/2)까지 있는 선물을 m_dst 벨트 앞으로 옮김
#    1개라면 안 옮김. 옮긴 뒤 m_dst에 선물 갯수 출력 

# 5. 선물 정보 얻기 prinT(a+2*b)
#    선물번호 주어질 때(p_num) 해당 선물선물의 앞 선물 번호a과 선물번호 b
#    앞에 없으면 a=-1 ,  뒤에 없으면 b=-1

# 6. 벨트 정보 얻기 print(a+2*b+3*c)
#    벨트 번호 b_num 주어지면 맨 앞에 a 맨 뒤 b. 선물갯수 c. 
#    없으면 a,b = -1, -1
Q = int(input()) # Q 줄 명령

### setting
### 100 n m B_NUM1 ... B_NUMm
q = list(map(int, input().split()))
n, m = q[1], q[2]

nums = [0] * (n+1) # belts들 몇개인지
head = [-1] * (n+1) # 벨트 앞에 있는게 뭔지
tail = [-1] * (n+1) # 벨트 뒤에 있는게 뭔지

belts = [[] for _ in range(n+1)] # 상품이 어느 belts위에 있는지
before = [-1] * (m+1) # 상품 앞 번호
after = [-1] * (m+1) # 상품 뒷 번호

# 벨트에 물건들 놓기
for i in range(1, m+1):
    belts[q[i+2]].append(i)
#print(belts)

# 각 상품들 정보 정리
for i in range(1, n+1):
    belt = belts[i]
    num_items = len(belt)
    nums[i] = num_items
    if num_items == 0:
        continue
    
    if num_items == 1:
        head[i] = belt[0]; tail[i] = belt[0]
        continue
    
    head[i] = belt[0]; tail[i] = belt[-1]
    after[belt[0]] = belt[1]
    before[belt[-1]] = belt[-2]
    num_items = len(belt)
    for i in range(1, num_items-1):
        after[belt[i]] = belt[i+1]
        before[belt[i]] = belt[i-1]
#print("NUM : ", nums[1:])
#print("HEAD : ", head[1:])
#print("TAIL : ", tail[1:])
#print("AFTER : ", after[1:])
#print("BEFORE : ", before[1:])
def Rule2(q):
    m_src, m_dst = q[1], q[2]
    num = nums[m_src]
    if num == 0: # 없으면 끝
        print(nums[m_dst])
        return
    nums[m_dst] += num; nums[m_src] = 0
    
    h = head[m_src]; head[m_src] = -1
    t = tail[m_src]; tail[m_src] = -1
    h_dst = head[m_dst]; before[h_dst] = t
    before[h] = -1
    after[t] = tail[m_dst]

    head[m_dst] = h
    if tail[m_dst] == -1:
        tail[m_dst] = t

    print(nums[m_dst])
    return
def Move(m_src, m_dst):
    item = tail[m_src]
    tail[m_src] = before[item] # m_src의 끝은 이제 item의 앞에 친구
    if tail[m_src] == -1: # 만약 비게 된다면
        head[m_src] = -1
    after[before[item]] = -1 # m_src의 끝 아이템의 뒤는 이제 없음 
    
    after[item] = head[m_dst] # 옮긴 물건은 m_dst의 맨 앞으로
    before[item] = -1 # 옮긴 물건은 맨 앞이라서 before가 없음

    before[head[m_dst]] = item # m_dst의 앞에 있는 애 앞에 생김. 뒤는 그대로
    
    head[m_dst] = item # head 없데이트
    nums[m_src] -= 1
    nums[m_dst] += 1
    return
def MoveFront(m_src, m_dst):
    #print("MOVE FRONT : ", m_src, m_dst)
    item = head[m_src] # item = 2
    head[m_src] = after[item] # m_src의 끝은 이제 item의 뒤에 친구 head[4] = after[2] = 3
    if head[m_src] == -1: # 만약 비게 된다면
        tail[m_src] = -1
    before[after[item]] = -1 # before[3] = -1
    
    after[item] = head[m_dst] # 옮긴 물건은 m_dst의 맨 앞으로. after[2] = -1
    before[item] = -1 # 옮긴 물건은 맨 앞이라서 before가 없음. after[2] = -1(맨 앞)

    if head[m_dst] != -1:
        before[head[m_dst]] = item # m_dst의 앞에 있는 애 앞에 생김. 뒤는 그대로. 
    
    head[m_dst] = item # head 없데m_
    if tail[m_dst] == -1: # 비어있었다면
        tail[m_dst] = item
    nums[m_src] -= 1
    nums[m_dst] += 1
    return
def Rule3(q): # 300 m_src m_dst
    m_src, m_dst = q[1], q[2]
    num_src = nums[m_src]; num_dst = nums[m_dst]
    if num_src == 0 and num_dst == 0:
        print(nums[m_dst])
        return
    if num_src == 0:
        MoveFront(m_dst, m_src)
        print(nums[m_dst])
        return
    
    if num_dst == 0:
        MoveFront(m_src, m_dst)
        print(nums[m_dst])
        return
    Move(m_src, m_dst)
    Move(m_dst, m_src)
    print(nums[m_dst])
    return
def Rule4(q): # 400 m_src m_dst
    m_src, m_dst = q[1], q[2]
    MoveFront(m_src, m_dst)
    print(nums[m_dst])
    return
def Rule5(q): # 500 p_num
    p_num = q[1]
    a = before[p_num]
    b = after[p_num]
    print(a + 2*b)
    return
def Rule6(q): # 600 b_num
    b_num = q[1]
    a = head[b_num]
    b = tail[b_num]
    c = nums[b_num]

    print(a + 2*b + 3*c)
    return

stop = -1
for i in range(1, Q):
    q = list(map(int, input().split()))
    if i == stop:
        print("TIME : ", i)
        print(q)
        
    elif q[0] == 200: # 200 m_src m_dst
        Rule2(q)
        
    elif q[0] == 300: # 300 m_src m_dst
        Rule3(q)

    elif q[0] == 400: # 400 m_src m_dst
        Rule4(q)
        
    elif q[0] == 500: # 500 p_num
        Rule5(q)
        
    elif q[0] == 600: # 600 b_num
        Rule6(q)
        
    
    if i == stop:
        print("NUM : ", nums[1:])
        print("HEAD : ", head[1:])
        print("TAIL : ", tail[1:])
        print("BEFORE : ", before[1:])
        print("AFTER : ", after[1:])

    #print(q)
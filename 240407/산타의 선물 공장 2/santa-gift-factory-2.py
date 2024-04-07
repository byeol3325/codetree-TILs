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
import heapq as hq
import sys
import copy

input = sys.stdin.readline 

Q = int(input()) # Q 줄 명령

def Setting(q):
    global belts, max_belts
    n = q[1]
    m = q[2]
    belts = [[] for _ in range(q[1]+1)] # 0, 1, 2, ... n-1
    max_belts = [[] for _ in range(q[1]+1)]
    for i in range(1, m+1):
        hq.heappush(belts[q[i+2]], i)
        hq.heappush(max_belts[q[i+2]], -i)
    #print(belts)
    #print(max_belts)
    return

def Rule2(q):
    global belts, max_belts
    m_src = q[1]; m_dst = q[2]
    n = len(belts[m_src])
    for _ in range(n):
        hq.heappush(belts[m_dst], hq.heappop(belts[m_src]))
        hq.heappush(max_belts[m_dst], hq.heappop(max_belts[m_src]))
    print(len(belts[m_dst]))
    return

# 3. 앞 물건만 교체 (m_src) <=> (m_dst)  ///  print(m_dst)
#    mm_src 벨트에 있는 선물 중 가장 앞에 있는 선물을 m_dst 벨트 선물들 중 가장 앞에 있는 선물과 교체
#   없으면 있는 곳에서만 옮기기 
#    옮긴 뒤에 m_dst벨트에 있는 선물 갯수 출력
def Rule3(q):
    global belts, max_belts
    m_src = q[1]; m_dst = q[2]
    n1 = len(belts[m_src]); n2 = len(belts[m_dst])
    src = []; max_src = [];
    dst = []; max_dst = [];
    if n1 != 0:
        n1_front = hq.heappop(belts[m_src])
        hq.heappush(dst, n1_front)
        hq.heappush(max_dst, -n1_front)
    
    if n2 != 0:
        n2_front = hq.heappop(belts[m_dst])
        hq.heappush(src, n2_front)
        hq.heappush(max_src, n2_front)
    
    for i in range(n1-1):
        n1_front = hq.heappop(belts[m_src])
        hq.heappush(src, n1_front)
        hq.heappush(max_src, -n1_front)
    
    for i in range(n2-1):
        n2_front = hq.heappop(belts[m_dst])
        hq.heappush(dst, n2_front)
        hq.heappush(max_dst, -n2_front)
    
    belts[m_src] = src; max_belts[m_src] = max_src
    belts[m_dst] = dst; max_belts[m_dst] = max_dst

    print(len(belts[m_dst]))
    return

# 4. 물건 나누기 (m_src) => (m_dst)    print(m_dst)
#    m_src 번째 벨트에 있는 선물 갯수 n이라고 할 때 가장 앞에앞에서 floor(n/2)까지 있는 선물을 m_dst 벨트 앞으로 옮김
#    1개라면 안 옮김. 옮긴 뒤 m_dst에 선물 갯수 출력 
def Rule4(q): # 400 m_src m_dst
    global belts, max_belts
    m_src = q[1]; m_dst = q[2]
    n1 = len(belts[m_src]); n2 = len(belts[m_dst])
    
    if n1 < 2:
        return
    
    mov_num = n1//2
    #if n1%2 == 1:
    #    mov_num += 1
    
    for _ in range(mov_num):
        n1_front = hq.heappop(belts[m_src])
        hq.heappush(belts[m_dst], n1_front)
        hq.heappush(max_belts[m_dst], -n1_front)
    
    max_src = []
    for v in belts[m_src]:
        hq.heappush(max_src, -v)
    
    max_belts[m_src] = max_src
    print(len(belts[m_dst]))
    return

def Rule5(q): # 500 p_num
    global belts, max_belts
    idx = 0
    for i, b in enumerate(belts):
        if q[1] in b:
            idx = i; break
    
    a = -1; b = -1;
    src = copy.deepcopy(belts[idx]); max_src = copy.deepcopy(max_belts[idx])

    while belts[idx]:
        now = hq.heappop(belts[idx])
        if now == q[1]:
            break
        a = now
    
    while max_belts[idx]:
        now = hq.heappop(max_belts[idx])
        if -now == q[1]:
            break
        b = -now
    
    belts[idx] = src; max_belts[idx] = max_src
    print(a + 2*b)
    return

def Rule6(q): # 600 b_num
    if len(belts[q[1]]) == 0:
        print(-3)
        return
    src = copy.deepcopy(belts[q[1]]); max_src = copy.deepcopy(max_belts[q[1]])
    a = hq.heappop(belts[q[1]]); b = -hq.heappop(max_belts[q[1]])
    belts[q[1]] = src; max_belts[q[1]] = max_src
    print(a + 2*b + 3*len(belts[q[1]]))
    return

belts = []; max_belts = [];
for i in range(Q):
    q = list(map(int, input().split()))
    if q[0] == 100: # 100 n m B_NUM1 B_NUM2 ... B_NUMm 항상 처음 명령. 출력할값 없음
        Setting(q)
        #print(belts[1:])
        #print(max_belts[1:])
        #pass
    elif q[0] == 200: # 200 m_src m_dst
        Rule2(q)
        #print(belts[1:])
        #print(max_belts[1:])
    elif q[0] == 300: # 300 m_src m_dst
        Rule3(q)
        #print("================== Time : ", i, "==================")
        #print(belts[1:])
        #print(max_belts[1:])
    elif q[0] == 400: # 400 m_src m_dst
        Rule4(q)
        #print("================== Time : ", i, "==================")
        #print(belts[1:])
        #print(max_belts[1:])
    elif q[0] == 500: # 500 p_num
        Rule5(q)
        #print("================== Time : ", i, "==================")
        #print(belts[1:])
        #print(max_belts[1:])
    elif q[0] == 600: # 600 b_num
        Rule6(q)
        #print("================== Time : ", i, "==================")
        #print(belts[1:])
        #print(max_belts[1:])
    
    #print(q)
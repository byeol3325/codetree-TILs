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
    global belts
    n = q[1]
    m = q[2]
    belts = [[] for _ in range(q[1]+1)] # 0, 1, 2, ... n-1
    for i in range(1, m+1):
        belts[q[i+2]].append(i)
    for i in range(n):
        belts[i+1].sort()
    return

def Rule2(q):
    global belts
    m_src = q[1]; m_dst = q[2]
    belts[m_dst] = belts[m_src] + belts[m_dst]
    belts[m_src] = []
    print(len(belts[m_dst]))
    return

# 3. 앞 물건만 교체 (m_src) <=> (m_dst)  ///  print(m_dst)
#    mm_src 벨트에 있는 선물 중 가장 앞에 있는 선물을 m_dst 벨트 선물들 중 가장 앞에 있는 선물과 교체
#   없으면 있는 곳에서만 옮기기 
#    옮긴 뒤에 m_dst벨트에 있는 선물 갯수 출력
def Rule3(q):
    global belts
    m_src = q[1]; m_dst = q[2]
    n1 = len(belts[m_src]); n2 = len(belts[m_dst])
    src = []
    dst = []
    if n1 == 0 and n2 == 0:
        print(0)
        return
    
    if n1 == 0:
        src = [belts[m_dst][0]]
        dst = belts[m_dst][1:]
    
    if n2 == 0:
        src = belts[m_src][1:]
        dst = [belts[m_src][0]]
    
    if n1 != 0 and n2 != 0:
        src = [belts[m_dst][0]] + belts[m_src][1:]
        dst = [belts[m_src][0]] + belts[m_dst][1:]
    
    belts[m_src] = src; belts[m_dst] = dst
    print(len(belts[m_dst]))
    return

# 4. 물건 나누기 (m_src) => (m_dst)    print(m_dst)
#    m_src 번째 벨트에 있는 선물 갯수 n이라고 할 때 가장 앞에앞에서 floor(n/2)까지 있는 선물을 m_dst 벨트 앞으로 옮김
#    1개라면 안 옮김. 옮긴 뒤 m_dst에 선물 갯수 출력 
def Rule4(q): # 400 m_src m_dst
    global belts, max_belts
    m_src = q[1]; m_dst = q[2]
    n1 = len(belts[m_src])
    
    if n1 < 2:
        return
    
    mov_num = n1//2
    #if n1%2 == 1:
    #    mov_num += 1
    src = belts[m_src][mov_num:]
    dst = belts[m_src][:mov_num] + belts[m_dst]
    
    belts[m_src] = src; belts[m_dst] = dst
    print(len(belts[m_dst]))
    return

def Rule5(q): # 500 p_num
    global belts, max_belts
    idx = 0; p_idx = -1
    for i, b in enumerate(belts):
        if q[1] in b:
            idx = i
            break
    
    p_idx = belts[idx].index(q[1])
    
    n = len(belts[idx])
    a = -1; b = -1;
    if p_idx != 0:
        a = belts[idx][p_idx-1]
    
    if p_idx != n-1:
        b = belts[idx][p_idx+1]
    #print("HERE A B :", idx, p_idx, a, b)
    print(a + 2*b)
    return

def Rule6(q): # 600 b_num
    if len(belts[q[1]]) == 0:
        print(-3)
        return
    a = belts[q[1]][0]; b = belts[q[1]][-1]
    print(a + 2*b + 3*len(belts[q[1]]))
    return

belts = []
tip = 100; stop = 100
for i in range(Q):
    q = list(map(int, input().split()))
    #if i >= tip:
    #    print("================== Time : ", i, "==================")
    #    print(q)

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
    
    #if i >= tip:
    #    print(belts[1:])
        
    #if i == stop:
    #    break
    #print(q)
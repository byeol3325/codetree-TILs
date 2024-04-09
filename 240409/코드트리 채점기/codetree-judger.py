# 코드트리 채점기

# Q번 명령. t 값은 항상 오름차순으로 들어옴

from collections import deque
import heapq as hq
################################# START #################################
### 입력 받기
Q = int(input())
### 세팅. 100 ~ 
# rule 1. "N개의 채점기". 초기문제 url에 해당하는 u0. (도메인/문제ID). 도메인은 알파벳 소문자 + '.' / ID는 숫자 (1~10억이하)
#           N개의 채점기에는 1~N번 번호. 0초에 채점 우선순위 1이면서 url이 u0인 초기 문제에 대한 채점 요청이 들어옴
#           채점 task는 채점 대기 큐에 들어감
#           100 N u0 : N개 채점기. 초기문제 url이 u0 항상 처음에 주어짐
settings = input().split()
N, u0 = int(settings[1]), settings[2]
u0 = u0.split('/')

calculaters = [[] for _ in range(N+1)] # 계산기 0 ~ N. 0번은 안 쓸거임
waiting_queue = [] # 대기 큐.
hq.heappush(waiting_queue, [1, 0, u0]) # 우선순위(p), 시간(t), [url, id] 어차피 오름차순 시간으로 들어옴.


# rule 2. 채점 요청. 대기 큐에 추가하면됨. t초, 채점 우선순위 p, url이 u 문제 채점 요청. 
#         u t p u : t초에 채점 우선순위가 p. url=u
def Rule2(q): # 200 t p u. 대기 큐에 추가하면됨.
    t, p, u = int(q[1]), int(q[2]), q[3]
    u = u.split('/')
    for task in waiting_queue: 
        if u == task[2]: # 단 대기 큐에 있는 task는 정확히 u와 일치하는 url이 단 하나라도 존재하면 큐에 추가하지 않고 넘어감
            #print("IN RULE2, SAME TASK IS IN QUEUE.")
            return
    hq.heappush(waiting_queue, ([p, t, u])) # 채점 task는 채점 대기 큐에.
    return

# rule 3. 채점 시도. t초에 채점 대기 큐에서 즉시 채점이 불가능한 경우를 제외하고 남은 task 중 우선순위가 가장 높은 채점 task를 골라 진행
#         task가 채점이 될 수 없는 조건. 1) 해당 task의 도메인이 현재 채점 진행중인 도메인 중 하나라면 불가능
#         2) task의 도메인이 정확히 일치하는 도메인에 대해 가장 최근 진행된 채점 시간이 start, 종료시간이 start+gap. 현재시간 t가 start + 3*gap보다 작다면 부적절한 채점 불가능
#         300 t : t초에 채점 대기 큐에서 즉시 채점이 가능한 경우 우선순위가 가장 높은거 골라서 채점 진행
#         즉시 채점 가능한 경우. 우선 순위가 가장 높은 채점 task 골라짐 1) 우선 순위p가 작을 수록 우선순위가 높음
#                                                                   2) 만약 채점 우선순위가 동일하다면 채점 task가 채점 대기 큐에 들어온 시간이 빠를 수록.
#         t초에 채점이 가능한 task가 단 하나라도 있었다면, 쉬고 있는 채점기 중 가장 번호가 작은 채점기가 우선순위가 가장 높은 채점 task에 대한 채점 시작
#          만약 쉬고 있는 채점기가 없다면 요청 무시하고 넘어가기
def Rule3(q): # 300 t. 채점해도되나 안되나 판별
    t = int(q[1])
    if len(waiting_queue) == 0: # 큐가 다 비었음
        #print("IN RULE3, NO QUEUE.")
        return

    ### 안되는 조건
    task = waiting_queue[0] # p, start_time, [도메인, id]
    domain = task[2][0]

    first_blank_ = -1 # 일단 제일 먼저 비어있는 계산기. 일단 기록.

    for i in range(1, N+1):
        if calculaters[i] == []:
            if first_blank_ == -1:
                first_blank_ = i
            continue
        else: 
            if domain == calculaters[i][2][0]: # 도메인 진행 중이라 불가능
                return
    
    if first_blank_ == -1: # 모든 계산기가 돌아가고 있음
        return

    if domain in end_task: # 만약 종료한적이 있으면
        start, end = end_task[domain]
        if t < start + 3*(end-start): # t가 start + 3gap보다 작으면 부적절한 채점이라 의심돼서 채점이 불가능함
            return
            
    # 됨. 쉬고 있는 계산기에 들어감
    task = hq.heappop(waiting_queue)
    task[1] = t # 시작시간
    calculaters[first_blank_] = task + [-1] # 종료시간 배정안됐으므로 -1
    return

# rule 4. 채점 종료. t초에 J_id 채점기가 진행하던 채점이 종료. J_id 채점기는 다시 쉬는 상태
#                 J_id번 채점기가 진행하던 채점이 없었다면 명령 무시
# 400 t J_id : t초에 J_id번 채점기가 진행하던 채점이 종료
end_task = {}
def Rule4(q): # 400 t J_id
    t, J_id = int(q[1]), int(q[2])

    if calculaters[J_id] == []: # 명령무시. j_id 번에 채점하는게 없으면 무시.
        return
    
    start_time = calculaters[J_id][1]
    end = t
    domain = calculaters[J_id][2][0]
    end_task[domain] = [start_time, end]
    calculaters[J_id] = [] # 다 끝났음. 삭제.
    return

# rule 5. 채점 대기 큐 조회. 시간 t에 채점 대기 큐에 있는 task 수 출력.
#           500 t : 시간 t에 채점 대기 큐에 있는 채점 task의 수 출력
def Rule5(q):
    t = int(q[1])
    print(len(waiting_queue))
    return

#print(waiting_queue)
stop = -1
for i in range(1, Q):
    q = input().split()

    #check_fin(int(q[1])) # 작업종료할게있는지 확인해야지

    if q[0] == "200":
        Rule2(q)
    elif q[0] == "300":
        Rule3(q)
    elif q[0] == "400":
        Rule4(q)
    elif q[0] == "500":
        Rule5(q)

    if i == stop:
        print("============= CHECK =============")
        print("command : ", i, q)
        print("TIME : ", q[1])
        print("waiting_queue : ", waiting_queue)
        print("calculaters : ", calculaters[1:])
        print("end_task : ", end_task)
        break


"""
# FOR TEST
print("FOR TEST")
a = [[1, 3], [1, 2]]
hq.heapify(a)
print(a)
hq.heappop(a)
print(a)
b = hq.heappop(a)
print(b)
b = hq.heappop(a)
print(b)
"""
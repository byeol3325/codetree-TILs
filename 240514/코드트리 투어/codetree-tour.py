# 여행사. n개 도시. 각 도시 사이 m개 간선. 도시는 0 ~ n-1. 
# 간선은 방향성X. 두 도시 사이 연결하는 간선은 여러개 존재 가능. 자기 자신에게 향하는 간선 존재 가능
# 출발지는 하나로 통일하여 관리. 처음 코드트리 여행 상품 출발지 0번

"""
100 n m v_1 u_1 w_1 v_2 u_2 w_2 ... v_m u_m w_m
"""
N, M = 0, 0
graph = []
def Rule1(q):
    global N, M, graph
    N, M = q[1], q[2]
    graph = [[] for _ in range(N)]
    for i in range(M):
        v, u, w = q[3+ 3*i], q[4+3*i], q[5+3*i]
        graph[v].append([u, w])
        graph[u].append([v, w])

    return None

def show_graph():
    global N, M, graph
    print("N, M : ", N, M)
    print("graph : ", graph)

"""
200 id revenue dest 에 해당하는 여행 상품 만들고 이를 관리 목록에 추가. 여행 상품이 고유 식별자 id 가지며, 도착지는 dest. 매출 revenue
주어지는 id는 모두 다름
"""
START = 0
class Item:
    def __init__(self, id_, revenue, dest, cost=0):
        self.id_ = id_
        self.revenue = revenue
        self.dest = dest
        self.cost = cost

    def show_item(self):
        print("show item id ", self.id_, "(revenue, dest, cost) : ", self.revenue, self.dest, self.cost)
        return None

    def change_cost(self):
        global START
        self.cost = get_cost2(self.dest)
        return None

Total_list = {} # id: item, 없애면 item이 아니라 -1로

from collections import deque

#using DFS
def get_cost(dest):
    global N, START, graph
    if dest == START:
        return 0

    costs = []
    q = deque()
    q.append([START, 0, [0]*(N)]) # [start, cost, [visited_list]]
    while q:
        info = q.popleft()
        v, c, visited = info[0], info[1], info[2]
        visited[v] = 1 #visit

        uws = graph[v]
        #print("UWS : ", uws)
        for uw in uws:
            u, w = uw[0], uw[1]
            next_visit = visited[:]
            if next_visit[u] == 1:
                continue
            else: # not visit
                new_cost = c + w
                if u == dest:
                    costs.append(new_cost)
                else:
                    q.append([u, new_cost, next_visit])

    if len(costs) != 0:
        return min(costs)
    else:
        return float("inf") # 최단 경로 없음

def get_cost2(dest):
    global N, START, graph
    if dest == START:
        return 0

    costs = [float("inf")]*N
    visited = [0] * N
    q = deque()
    q.append([START, 0])

    while q:
        v, c = q.popleft()
        visited[v] = 1 # visit
        
        uws = graph[v]
        for uw in uws:
            u, w = uw[0], uw[1]
            new_cost = c + w
            if costs[u] > new_cost:
                costs[u] = new_cost
                if visited[u] == 0:
                    q.append([u, new_cost])

    return costs[dest]

def Rule2(q):
    global N, graph, Total_list, START
    id_, revenue, dest = q[1], q[2], q[3]
    cost = get_cost2(dest)
    item = Item(id_, revenue, dest, cost)
    Total_list[id_] = item
    return None

"""
300 id. 해당 id 여행 상품 존재 시, 해당 id의 여행 상품을 관리 목록에서 삭제
"""
def Rule3(q):
    global Total_list
    id_ = q[1]
    if id_ in Total_list:
        Total_list.pop(id_)
    return None


"""
400.   revenue-cost가 최대인 상품을 우선적으로 고려. 같은 값을 가지는 상품이 여러 개 있을 경우 id가 작은 상품 선택.
cost는 현재 여행 상품의 출발지로부터 id 상품의 도착지까지 도달하기 위한 최단 거리
만약 출발지에서 dest로 도달하는 것이 불가능하거나 cost가 revenue보다 값이 커서 여행사가 이득을 얻을 수 없는 상황이면 판매 불가 상품.
판매 가능한 상품 중 가장 우선순위가 높은 상품을 1개 판매하게 되며, 이 상품의 id를 출력한 뒤 이 상품을 관리 목록에서 제거.
판매 가능한 상품이 전혀 없으면 -1 출력. 상품 제거 X
"""
def Rule4(q):
    global Total_list
    lists = []
    for k, v in Total_list.items():
        if v.revenue - v.cost < 0:
            continue
        lists.append([v.revenue - v.cost, -k])
    lists.sort(reverse=True)
    #print(lists)
    if len(lists) == 0 or lists[0][0] < 0:
        print(-1)
    else:
        id_ = -lists[0][1]
        print(id_)
        Total_list.pop(id_) # 제거
    return None

"""
500 s. 여행 상품의 출발지를 모두 s로 변경. cost가 변경될 수 있음
"""
def Rule5(q):
    global START, Total_list
    START = q[1]
    for k, v in Total_list.items():
        v.change_cost()
    return None

def show_all():
    global Total_list
    for k, v in Total_list.items():
        v.show_item()

    return

#import sys
#sys.stdin = open("example1.txt", "r")

Q = int(input())
stop = -1
for i in range(1, Q+1):
    q = list(map(int, input().split()))

    if q[0] == 100:
        Rule1(q)
    elif q[0] == 200:
        Rule2(q)
    elif q[0] == 300:
        Rule3(q)
    elif q[0] == 400:
        Rule4(q)
    else: # q[0] == 500
        Rule5(q)

    if stop == i:
        print("command : ", q)
        show_graph()
        show_all()
        break
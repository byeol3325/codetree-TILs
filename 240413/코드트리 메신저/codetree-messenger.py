from collections import deque

N, Q = map(int, input().split())

chat_rooms = {}
class ChatRoom:
    def __init__(self, parent, authority, alarm=True, nodes=None):
        self.parent = parent
        self.authority = authority
        self.alarm = alarm
        self.nodes = nodes if nodes is not None else set()

    def turn_ONOFF(self):
        self.alarm = not self.alarm
    
    def change_POWER(self, p):
        self.authority = p
    
    def get_nodes(self, n):
        self.nodes.add(n)
    
    def change_node(self, node, new_node):
        self.nodes.remove(node)
        self.nodes.add(new_node)
    
    def getINFO(self):
        return [self.parent, self.authority, self.alarm, self.nodes]

def build_tree(parents_authorities):
    global chat_rooms, N
    chat_rooms[0] = ChatRoom(None, 1, None) # 메인 채팅방
    for i in range(1, N + 1):
        power = parents_authorities[i+N]
        if power > 20:
            power = 21
        chat_rooms[i] = ChatRoom(parents_authorities[i], power)
    
    for i in range(1, N + 1):
        chat_rooms[chat_rooms[i].parent].get_nodes(i)
    return

def swap_parents(idx1, idx2):
    global chat_rooms
    #print("do swap")
    parent1 = chat_rooms[idx1].parent
    parent2 = chat_rooms[idx2].parent
    if parent1 == parent2:
        return
    chat_rooms[idx1].parent = parent2
    chat_rooms[idx2].parent = parent1

    chat_rooms[parent1].change_node(idx1, idx2)
    chat_rooms[parent2].change_node(idx2, idx1)
    return

def count_notifiable2(idx):
    global chat_rooms, N
    count = 0
    for i in range(1, N+1):
        if i == idx:
            continue
        depth = 1
        power = chat_rooms[i].authority
        node = chat_rooms[i].parent
        #print("now start node idx, i: ", idx, i)
        if chat_rooms[i].alarm == False:
            continue

        while True:
            if node == idx and depth <= power:
                #print("*** node linked to idx : ", i)
                count += 1
                break

            if node == None:
                #print("not linked to idx : ", i)
                break
            
            if chat_rooms[node].alarm == False:
                #print("not linked to idx : ", i)
                break
            
            if chat_rooms[node].parent == None:
                #print("not linked to idx : ", i)
                break
            
            node = chat_rooms[node].parent
            depth += 1
    print(count)
    return
            

def count_notifiable(idx):
    global chat_rooms, N
    count = 0
    
    if len(chat_rooms[idx].nodes) == 0: # nodes가 없음
        print(count)
        return

    q = deque()
    for n in chat_rooms[idx].nodes:
        q.append(n)
    
    depth = 1
    while True:
        same_depth_nodes = len(q)
        for _ in range(same_depth_nodes):
            node = q.popleft()
            if chat_rooms[node].alarm == False: # 끊겨있음
                continue
            #print(node, "node info(parent, power, alarm, nodes) : ", chat_rooms[node].getINFO())
            if chat_rooms[node].authority >= depth: # 목소리가 닿음
                count += 1
            for n in chat_rooms[node].nodes: # 밑에 노드들도 확인
                q.append(n)
        #print("check next_q : ", next_q)
        if len(q) == 0: # 다음에 더 갈게 없음
            break
        depth += 1
    
    print(count)
    return 

#parents_authorities = list(map(int, input().split())) # 100 p1 p2 ... pN a1 a2 ... aN

stop = -1
#show_chat_rooms = 1
for i in range(1, Q+1):
    q = list(map(int, input().split()))
    #if stop == i:
    #    print("TURN : ", i, q)
    #    print("Before : ")
    #    if show_chat_rooms == 1:
    #        for c in range(1, N+1):
    #            print(c, "chat room info(parent, power, alarm, nodes) : ", chat_rooms[c].getINFO())

    if q[0] == 100: # 100 p1 p2 ... pN a1 a2 ... aN
        build_tree(q)
    elif q[0] == 200: # 200 c
        chat_rooms[q[1]].turn_ONOFF()
    elif q[0] == 300: # 300 c power
        chat_rooms[q[1]].change_POWER(q[2])
    elif q[0] == 400: # 400 c1 c2
        swap_parents(q[1], q[2])
    else: # 500 c
        count_notifiable2(q[1])
    
    if stop == i:
    #    print("After : ")
    #    if show_chat_rooms == 1:
    #        for c in range(1, N+1):
    #            print(c, "chat room info(parent, power, alarm, nodes) : ", chat_rooms[c].getINFO())
        break
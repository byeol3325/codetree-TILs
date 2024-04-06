#import sys
#sys.setrecursionlimit(10**6)

class ChatRoom:
    def __init__(self, parent, authority, alarm=True, nodes=[]):
        self.parent = parent
        self.authority = authority
        self.alarm = alarm
        self.nodes = nodes

def build_tree(N, parents_authorities):
    chat_rooms = [ChatRoom(None, 1, False)]  # 메인 채팅방
    for i in range(1, N + 1):
        chat_rooms.append(ChatRoom(parents_authorities[i], parents_authorities[i+N]))
    
    for i in range(N+1):
        parent = chat_rooms[i].parent
        if parent == None:
            continue
        else:
            if chat_rooms[parent].nodes == []:
                chat_rooms[parent].nodes = [i]
            else:
                chat_rooms[parent].nodes += [i]
    return chat_rooms

def switch_notification(chat_rooms, idx):
    chat_rooms[idx].alarm = not chat_rooms[idx].alarm

def change_power(chat_rooms, idx, power):
    chat_rooms[idx].authority = power

def swap_parents(chat_rooms, idx1, idx2):
    # 4, 5
    parent1 = chat_rooms[idx1].parent # 1
    parent2 = chat_rooms[idx2].parent # 2
    if parent1 == parent2:
        return

    chat_rooms[parent1].nodes = [node for node in chat_rooms[parent1].nodes if node != idx1] + [idx2]
    chat_rooms[parent2].nodes = [node for node in chat_rooms[parent2].nodes if node != idx2] + [idx1]

    chat_rooms[idx1].parent, chat_rooms[idx2].parent = chat_rooms[idx2].parent, chat_rooms[idx1].parent

def count_notifiable(chat_rooms, idx, depth):
    global N, count
    if depth <= chat_rooms[idx].authority:
        if depth != 0:
            #print("Node : ", idx)
            count+=1
    
    nodes = chat_rooms[idx].nodes
    
    for node in nodes:
        if chat_rooms[node].alarm == True:
            count_notifiable(chat_rooms, node, depth+1)
    return 

N, Q = map(int, input().split())
parents_authorities = list(map(int, input().split())) # 100 p1 p2 ... pN a1 a2 ... aN
chat_rooms = build_tree(N, parents_authorities)

for _ in range(1, Q):
    q = list(map(int, input().split()))
    if q[0] == 200: # 200 c
        switch_notification(chat_rooms, q[1])
    elif q[0] == 300: # 300 c power
        change_power(chat_rooms, q[1], q[2])
    elif q[0] == 400: # 400 c1 c2
        swap_parents(chat_rooms, q[1], q[2])
    else: # 500 c
        count = 0
        count_notifiable(chat_rooms, q[1], 0)
        print(count)
    
    #for i in range(N+1):
    #    print(i, chat_rooms[i].nodes)
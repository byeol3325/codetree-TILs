#import sys
#sys.setrecursionlimit(10**6)
import copy

class ChatRoom:
    def __init__(self, parent, authority, alarm, nodes):
        self.parent = parent
        self.authority = authority
        self.alarm = alarm
        self.nodes = nodes

def build_tree(N, parents_authorities):
    chat_rooms = [ChatRoom(None, 1, True, []) for _ in range(N+1)]  # 메인 채팅방
    for i in range(1, N + 1):
        parent = parents_authorities[i]
        chat_rooms[i].parent = parent
        chat_rooms[i].authority = parents_authorities[i+N]
        chat_rooms[parent].nodes = copy.copy(chat_rooms[parent].nodes)
        chat_rooms[parent].nodes.append(i)
    return chat_rooms

def switch_notification(chat_rooms, idx):
    chat_rooms[idx].alarm = not chat_rooms[idx].alarm

def change_power(chat_rooms, idx, power):
    chat_rooms[idx].authority = power

def swap_parents(chat_rooms, idx1, idx2):
    parent1 = chat_rooms[idx1].parent
    parent2 = chat_rooms[idx2].parent
    if parent1 == parent2:
        return

    chat_rooms[parent1].nodes.remove(idx1)
    chat_rooms[parent1].nodes.append(idx2)
    chat_rooms[parent2].nodes.remove(idx2)
    chat_rooms[parent2].nodes.append(idx1)

    chat_rooms[idx1].parent, chat_rooms[idx2].parent = parent2, parent1


def count_notifiable(chat_rooms, idx, depth):
    count = 0
    stack = [(idx, 0)]  # (node index, depth)

    while stack:
        node_idx, depth = stack.pop()
        if depth <= chat_rooms[node_idx].authority and depth != 0:
            count += 1

        for child_idx in chat_rooms[node_idx].nodes:
            if chat_rooms[child_idx].alarm:
                stack.append((child_idx, depth + 1))
    print(count)

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
        #count = 0
        count_notifiable(chat_rooms, q[1], 0)
        #print(count)
    
    #for i in range(N+1):
    #    print(i, chat_rooms[i].nodes)
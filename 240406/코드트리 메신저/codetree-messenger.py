class ChatRoom:
    def __init__(self, parent, authority, alarm=True):
        self.parent = parent
        self.authority = authority
        self.alarm = alarm

def build_tree(N, parents_authorities):
    chat_rooms = [ChatRoom(None, 1, None)]  # 메인 채팅방
    for i in range(1, N + 1):
        chat_rooms.append(ChatRoom(parents_authorities[i], parents_authorities[i+N]))
    return chat_rooms

def switch_notification(chat_rooms, idx):
    chat_rooms[idx].alarm = not chat_rooms[idx].alarm

def change_power(chat_rooms, idx, power):
    chat_rooms[idx].authority = power

def swap_parents(chat_rooms, idx1, idx2):
    chat_rooms[idx1].parent, chat_rooms[idx2].parent = chat_rooms[idx2].parent, chat_rooms[idx1].parent

def count_notifiable(chat_rooms, idx):
    global N
    count = 0
    for i in range(N+1):
        if i == idx: # 본인 제외
            continue
        
        chat_room = chat_rooms[i]
        power = chat_room.authority
        not_me = 1
        while True:
            if chat_room.alarm == False: # 위로 못 올림
                break
            if not_me == 1:
                not_me -= 1
            else:
                power -= 1

            if chat_room.parent == idx: # 받으면 숫자 세봄
                if power > 0:
                    count += 1
            if chat_room.parent == None: # 끝까지 올려봤는데도 없음
                break 
            chat_room = chat_rooms[chat_room.parent]
    print(count)
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
        count_notifiable(chat_rooms, q[1])
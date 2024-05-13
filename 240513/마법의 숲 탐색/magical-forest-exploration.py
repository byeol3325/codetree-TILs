# R행, C열. 가장 위를 1행, 아래를 R행
# 숲의 동쪽, 서쪽, 남쪽은 마법의 벽으로 막혀 정령들은 숲의 북쪽으로만 숲에 들어올 수 있음

# K 명의 정령. 골렘 타고 숲을 탐색. 골램은 십자 모양 구조. 중앙 포함 5칸. 중앙 제외한 4칸 중 하나는 골렘의 출구.
# 어느 방향에서도 탑승가능하지만 내릴 때는 정해진 출구로 내릴 수 있음

# i 번째로 숲을 탐색하는 골렘 가장 북쪽에서 시작. 중앙이 c_i열이 되도록 하는 위치에서 내려오기 시작.
# 초기 골렘의 출구는 d_i의 방향에 위치
# 밑에 뭐가 있다면 서쪽(x -1)로 회전하면서 내려감. 반시계방향으로 이동
# 밑과 그리고 서쪽 밑 혹은 서쪽에 뭐가 있으면 동쪽으로감. 시계방향
# 도달할 수 있는 가장 남쪽에 도달하면(y가장 큼) 정령은 골렘 내에서 상하좌우 인접한 칸으로 이동
# 단, 골렘 출구가 다른 골렘과 인접하고 있으면 해당 출구를 통해 다른 골렘으로 이동할 수 있음
# 모든 골렘이 남쪽으로 이동했지만 골렘 몸 일부가 여전히 숲을 벗어난 상태라면 해당 골렘을 포함해 숲에 위치한 있던 모든 골렘들은 다 나가고 
# 나갔던 골렘부터 다시 탐색.
# 정령이 도달하는 최종 위치를 답에 포함X

# 각 정령들이 최종적으로 위치한 행의 총합을 구하는 프로그램을 작성
# 숲이 다시 텅 비게 되더라도 행의 총합은 누적.

from collections import deque

R, C, K = map(int, input().split())
CDs = [list(map(int, input().split())) for _ in range(K)] #c_i, d_i K개

DIRECTION = [[-1, 0], [0, 1], [1, 0], [0, -1]] #북 동 남 서. 시계방향 +1
BOARD = [[0]*(C+1) for _ in range(R+1)]

RESET_OPT = 0
class Angel:
    def __init__(self, info):
        self.all_ = [[1, info[0]]] # center + side(북,동,남,서)
        for i in range(4):
            self.all_.append([1+DIRECTION[i][0], info[0]+DIRECTION[i][1]])
        self.outlet = info[1] # direction idx
    
    def show_info(self):
        """
        show next info about Angel. (center, outlet)
        
        Returns:
          0,1,2 => down, left, right
        """
        print("center, outlet : ", self.all_[0], self.outlet)

    def move_once(self):
        global BOARD, R, C, RESET_OPT
        """
        check next mov. self.all_ : center, 북, 동, 서, 남
        Returns:
          0,1,2 => down, left, right
        """
        RESET_OPT = 0
        
        # 끝까지 다 움직인 상태
        if self.all_[3][0] == R:
            return False

        # 움직이기 전 자기자리 비우기
        for i in range(5):
            BOARD[self.all_[i][0]][self.all_[i][1]] = 0

        # down(y: +1), 2 3 4
        check_down = [self.all_[2], self.all_[3], self.all_[4]]
        no_down = 0
        for cd in check_down:
            if BOARD[cd[0]+1][cd[1]] != 0:
                no_down = 1; break
        
        if no_down == 0:
            for i in range(5):
                self.all_[i][0] += 1
                BOARD[self.all_[i][0]][self.all_[i][1]] = 1
            return True            
        
        # left(x: -1), 1 3 4
        # left, down 고려해야함. self.outlet -= 1
        check_left = [self.all_[1], self.all_[3], self.all_[4], [self.all_[4][0]+1, self.all_[4][1]], [self.all_[3][0]+1, self.all_[3][1]]]
        no_left = 0
        for cl in check_left:
            if cl[1]-1 <= 0 or BOARD[cl[0]][cl[1]-1] != 0:
                no_left = 1; break
        
        if no_left == 0:
            for i in range(5):
                self.all_[i][0] += 1; self.all_[i][1] -= 1
                BOARD[self.all_[i][0]][self.all_[i][1]] = 1
            self.outlet = (self.outlet-1)%4
            return True
        
        # right(x: +1) 1 2 3
        # right, down 고려. self.outlet += 1
        check_right = [self.all_[1], self.all_[2], self.all_[3], [self.all_[2][0]+1, self.all_[2][1]], [self.all_[3][0]+1, self.all_[3][1]]]
        no_right = 0
        for cr in check_right:
            if cr[1]+1 > C or BOARD[cr[0]][cr[1]+1] != 0:
                no_right = 1; break
        
        if no_right == 0:
            for i in range(5):
                self.all_[i][0] += 1; self.all_[i][1] += 1
                BOARD[self.all_[i][0]][self.all_[i][1]] = 1
            self.outlet = (self.outlet+1)%4
            return True
        
        # 안 움직임
        # 움직이기 전 자기자리 비우기
        for i in range(5):
            BOARD[self.all_[i][0]][self.all_[i][1]] = 1
        
        if self.all_[1][0] <= 0:
            RESET_OPT = 1
            reset_board()

        return False

    def get_score(self, reset_opt=0):
        global DIRECTION, BOARD, R, C
        if reset_opt == 1:
            return 0

        start = [self.all_[0][0] + DIRECTION[self.outlet][0], self.all_[0][1] + DIRECTION[self.outlet][1]]
        q = deque()
        q.append(start)
        max_R = 0
        check_BOARD = [[0]*(C+1) for _ in range(R+1)]

        go_others = 0
        for i in range(4):
            ny = start[0] + DIRECTION[i][0]; nx = start[1] + DIRECTION[i][1]
            if ny <= 0 or nx <= 0 or ny > R or nx > C:
                continue
            if BOARD[ny][nx] == 1 and [ny, nx] not in self.all_:
                go_others = 1
                break
        
        if go_others == 0:
            return max(self.all_)[0]

        while q:
            loc = q.popleft()
            check_BOARD[loc[0]][loc[1]] = 1

            if loc[0] > max_R:
                max_R = loc[0]
            
            for i in range(4):
                ny = loc[0] + DIRECTION[i][0]; nx = loc[1] + DIRECTION[i][1]
                if ny <= 0 or nx <= 0 or ny > R or nx > C:
                    continue
                
                if BOARD[ny][nx] == 1 and check_BOARD[ny][nx] == 0:
                    q.append([ny, nx])
        
        return max_R

# get info about Angels
Angels = [Angel(CDs[i]) for i in range(K)]

def reset_board():
    global BOARD, R, C
    BOARD = [[0]*(C+1) for _ in range(R+1)]
    RESET_OPT = 1
    return None

def move(angel):
    while True:
        result = angel.move_once()
        
        if result == False: # no move
            break
    return None

def solution(stop=-1):
    total = 0
    for i in range(K):
        if stop == i:
            #angel.show_info()
            break
        angel = Angels[i]

        #print("before angel BOARD : ", i)
        #show_board()
        move(angel)
        total += angel.get_score(RESET_OPT)
        #print("after angel BOARD : ", i)
        #show_board()
        
    return total

def show_board():
    for i in range(1, R+1):
        print(BOARD[i][1:])




#Angels[4].show_info()
show_idx = -1
#Angels[show_idx-1].show_info()
result = solution(show_idx)
#Angels[show_idx-1].show_info()
#print("SHOW BOARD")
#show_board()
print(result)
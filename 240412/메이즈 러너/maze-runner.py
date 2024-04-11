import heapq as hq

N, M, K = map(int, input().split())
matrix = [list(map(int, input().split())) for _ in range(N)]
people = [list(map(int, input().split())) for _ in range(M)]
for p in people:
    p[0] -= 1; p[1] -= 1
#print("PEOPLE : ", people)
exit = list(map(int, input().split()))
exit[0] -= 1; exit[1] -= 1
TOTAL_DISTANCE = 0

def Rot90_matrix(start, end):
    global matrix, N
    # start = [왼쪽 위], end = 오른쪽 아래(그림상) => r작, c작 / r큰 c큰
    l = end[0] - start[0] + 1
    start_h = start[0]; start_w = start[1]
    end_h = end[0]; end_w = end[1]
    temp_matrix = [[0] * l for _ in range(l)]
    for i in range(l):
        for j in range(l):
            temp_matrix[j][l - 1 - i] = matrix[i + start_h][j + start_w]

    # 임시 행렬에서 원래 행렬로 복사
    for i in range(l):
        for j in range(l):
            if temp_matrix[i][j]-1 <= 0:
                matrix[i + start_h][j + start_w] = 0
            else:
                matrix[i + start_h][j + start_w] = temp_matrix[i][j]-1
    return

def Rot90_elements(start, end):
    # 출구 및 사람 돌리기
    global people, exit
    l = end[0] - start[0] + 1
    start_h = min(start[0], end[0]); start_w = min(start[1], end[1])
    end_h = max(start[0], end[0]); end_w = max(start[1], end[1])

    for i in range(len(people)):
        x, y = people[i][0], people[i][1]
        if start_h <= x <= end_h and start_w <= y <= end_w:
            x-=start_h; y-=start_w
            RotX = y+start_h; RotY = l-1-x+start_w
            people[i] = [RotX, RotY]
    
    if start_h <= exit[0] <= end_h and start_w <= exit[1] <= end_w:
        x, y = exit[0], exit[1]
        x-=start_h; y-=start_w
        RotX = y+start_h; RotY = l-1-x+start_w
        exit = [RotX, RotY]
    return

dy = [-1,1,0,0]; dx = [0,0,-1,1]
def Distance(A, B):
    return abs(A[0]-B[0]) + abs(A[1]-B[1])
def Go():
    # 사람들 한번 Go
    global people, TOTAL_DISTANCE, dx, dy, matrix, exit
    
    next_people = []
    for p in people:
        ori_dis = Distance(p, exit)
        stop = 0
        #print("person : ", p)
        for i in range(4):
            np = [p[0]+dy[i], p[1]+dx[i]]
            if np == exit: # 오.. 이사람 탈출함. 다시 추가안해도됨
                TOTAL_DISTANCE += 1
                #print("EXIT!!!!")
                break
            #print("person, next person : ", p, np)
            if Distance(np, exit) < ori_dis and matrix[np[0]][np[1]] == 0: # (벽 아님)한칸 이동 + 거리 줄어듦
                next_people.append(np) 
                TOTAL_DISTANCE += 1
                break
            else: # 갈 수가 없어서 다른 경로 탐색
                stop += 1
    
        if stop == 4: # 벽이 있어서 갈 데가 없음 못 옮김
            next_people.append(p)

    people = next_people  
    return

def GetLocation():
    # 회전할 구역 구하기
    global people, dx, dy, exit
    All_info = [] # dis, [r, c]
    for i,p in enumerate(people):
        hq.heappush(All_info, [Distance(p, exit), p])
    
    min_ = All_info[0][1]
    l = max(abs(exit[0]-min_[0]), abs(exit[1]-min_[1]))+1
    up = min(min_[0], exit[0]); left = min(min_[1], exit[1])
    down = max(min_[0], exit[0]); right = max(min_[1], exit[1])
    start = [0, 0]
    if up > l:
        start[0] = up-(l-1)
    if left > l :
        start[1] = left - (l-1)
    
    for i in range(l+1):
        if start[0] + i + l-1 >= down:
            start[0] += i
            break
    
    for i in range(l+1):
        if start[1] + i + l-1 >= right:
            start[1] += i
            break
    
    return start, [start[0]+l-1, start[1]+l-1]
    

    """
    print("HERE : All_info, min_", All_info, min_)
    l = max(abs(exit[0]-min_[0]), abs(exit[1]-min_[1]))
    
    A_to_B = [min_[0] - exit[0], min_[1] - exit[1]]
    start_AtoB = exit
    B_to_A = [exit[0] - min_[0], exit[1] - min_[1]]
    start_BtoA = min_
    
    if A_to_B[0] == 0:
        A_to_B[0] = 1; B_to_A[0] = -1
    
    if A_to_B[1] == 0:
        A_to_B[1] = 1; B_to_A[1] = -1
    #print("HERE : ", A_to_B, B_to_A)
    end_AtoB = [exit[0]+int(A_to_B[0]/abs(A_to_B[0])*l), exit[1]+int(A_to_B[1]/abs(A_to_B[1])*l)]
    end_BtoA = [min_[0]+int(B_to_A[0]/abs(B_to_A[0])*l), min_[1]+int(B_to_A[1]/abs(B_to_A[1])*l)]
    #print("HERE start, end AtoB: ", start_AtoB, end_AtoB)
    #print("HERE start, end BtoA: ", start_BtoA, end_BtoA)
    AtoB = []; hq.heappush(AtoB, start_AtoB); hq.heappush(AtoB, end_AtoB)
    BtoA = []; hq.heappush(BtoA, start_BtoA); hq.heappush(BtoA, end_BtoA)

    AtoB = [AtoB[0][0], AtoB[1][1], AtoB[1][0], AtoB[0][1]]
    BtoA = [BtoA[0][0], BtoA[1][1], BtoA[1][0], BtoA[0][1]]
    if AtoB[0] < 0:
        AtoB[2] -= AtoB[0]; AtoB[0] = 0
    if AtoB[1] < 0:
        AtoB[3] -= AtoB[1]; AtoB[1]
    print("HERE AtoB: ", AtoB)
    print("HERE BtoA: ", BtoA)
    for a in AtoB:
        if a < 0:
            return BtoA[:2], BtoA[2:]
    
    for b in BtoA:
        if b < 0:
            return AtoB[:2], AtoB[2:]

    All_ = []; hq.heappush(All_, AtoB); hq.heappush(All_, BtoA)
    
    #print(All_)
    if All_[0][0] >= 0:
        return All_[0][:2], All_[0][2:]
    else:
        return All_[1][:2], All_[1][2:]
    """

stop = -1
for k in range(1, K+1):
    if k == stop:
        print("TURN : ", k)
    # 이동
    Go()
    # 모든 참가자들이 미로를 탈출
    if len(people) == 0:
        break

    #start, end = GetLocation()
    #Rot90_matrix(start, end) # matrix 회전
    #Rot90_elements(start, end) # 사람들과 exit 회전
    start, end = GetLocation()
    Rot90_matrix(start, end)
    Rot90_elements(start, end)
    #if k != stop:#
        # 회전할 구역 구하고
    #    start, end = GetLocation()
        # 회전
    #    Rot90_matrix(start, end) # matrix 회전
    #    Rot90_elements(start, end) # 사람들과 exit 회전

    if k == stop:
        print("=============== MATRIX ===============")
        for i in range(N):
            print(matrix[i])
        print("start, end : ", start, end)
        print("people : ", people)
        print("exit : ", exit)
        break

print(TOTAL_DISTANCE)
print(exit[0]+1, exit[1]+1)


"""

print("=============== MATRIX ===============")
for i in range(N):
    print(matrix[i])

Rot90_matrix([1,0], [4,3])
print("=============== Rot90 MATRIX ===============")
for i in range(N):
    print(matrix[i])
"""
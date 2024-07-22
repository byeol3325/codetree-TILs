def solution(n: int):
    board = [[0]*n for _ in range(n)]

    # 우하좌상
    # 5 4 4 3 3 2 2 1 1
    directions = [[0,1],[1,0],[0,-1],[-1,0]]

    point = [0,0]
    num = 1
    d = 0

    board[0][0] = num
    num += 1
    for i in range(n-1): # 첫번째 줄
        point[0] = point[0]+directions[d][0]
        point[1] = point[1]+directions[d][1]
        board[point[0]][point[1]] = num
        num += 1
    d += 1
    
    for length in range(n-1, 0, -1):
        for _ in range(2):
            for i in range(1, length+1):
                point[0] = point[0]+directions[d][0]
                point[1] = point[1]+directions[d][1]
                board[point[0]][point[1]] = num
                num += 1
            d = (d+1)%4
    return board



def show_matrix(matrix: list):
    for i in range(len(matrix)):
        print(*matrix[i])


n = int(input())
board = solution(n)
show_matrix(board)
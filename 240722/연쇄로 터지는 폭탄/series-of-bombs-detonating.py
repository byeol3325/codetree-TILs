from collections import deque

def bfs(idx: int, locations: list):
    n = len(locations)
    answer = 1
    L, R = idx, idx

    boom = 1
    while L != -1 and R != -1:
        if L != 0 and locations[L] - locations[L-1] <= boom:
            answer += 1
            L = L-1
        else:
            L = -1

        if R != n-1 and locations[R+1] - locations[R] <= boom:
            answer += 1
            R = R+1
        else:
            R = -1
        boom += 1
    return answer
        


def solution(locations: list) -> int:
    locations = sorted(locations)
    n = len(locations)

    answers = [0] * n
    for i in range(n):
        answers[i] = bfs(i, locations)
    
    print(max(answers))
    
    return None

N = int(input())
locations = [int(input()) for _ in range(N)]
solution(locations)
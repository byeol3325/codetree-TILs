def solution(locations: list):
    locations = sorted(locations) # 정렬하고
    n = len(locations) # 갯수 세기

    def boom_idx(idx: int):
        """
        idx 번째 폭탄 boom 했을 때 터지는 폭탄 갯수
        """
        answer = 1
        L, R = idx, idx
        boom_range = 1

        while True:
            num_L, num_R = 0, 0
            if R != n-1:
                while locations[R+num_R+1] - locations[R] <= boom_range:
                    num_R += 1

                    if R+num_R+1 > n-1:
                        break
                if num_R == 0:
                    R = n-1
                else:
                    answer += num_R
                    R += num_R
                    
            if L != 0:
                while locations[L] - locations[L-num_L-1] <= boom_range:
                    num_L += 1
                    if L-num_L-1 < 0:
                        break
                if num_L == 0:
                    L = 0
                else:
                    answer += num_L
                    L -= num_L
                    
            if L == 0 and R == n-1:
                break
            boom_range+=1
        return answer
    
    answers = [0] * n
    for i in range(n):
        answers[i] = boom_idx(i)
    print(max(answers))
    return None


N = int(input())
locations = [int(input()) for _ in range(N)]
solution(locations)
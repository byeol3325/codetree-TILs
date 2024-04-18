A, N, B = map(int, input().split())

strN = str(N)
lenN = len(strN)
realA = 0
digit = 1
for i in range(lenN):
    realA += digit*int(strN[-1-i])
    digit *= A

NB = ""
digit = B
# 63 => 63%2 + 62%4 + 60%8 + 56%16 + 48%32 + 16% 
#       31 
while True:
    NB =  str(realA%digit) + NB
    realA = realA//digit
    
    if realA == 0:
        break
    else:
        digit *= B

print(NB)
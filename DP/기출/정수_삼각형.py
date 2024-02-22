# 답지가 내 풀이와 Same

n = int(input())
dp = []

for _ in range(n):
    dp.append(list(map(int,input().split())))

# 2번째 줄부터 내려가며 확인
for i in range(1,n):
    
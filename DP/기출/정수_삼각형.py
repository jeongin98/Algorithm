# 답지가 내 풀이와 Same

n = int(input())
dp = []

for _ in range(n):
    dp.append(list(map(int,input().split())))

# 2번째 줄부터 내려가며 확인
for i in range(1,n):
    for j in range(i+1):
        # 왼쪽 위에서 내려오는 경우([i-1][j-1])
        if j == 0: # 첫 인덱스일 경우
            up_left = 0
        else:
            up_left = dp[i-1][j-1]
        # 바로 위에서 내려오는 경우([i-1][j])
        if j == i:
            up = 0
        else:
            up = dp[i-1][j]
        # 최대 합을 저장
        dp[i][j] = dp[i][j] + max(up_left, up)

# 마지막 줄 중에서 최대 dp값 찾기
# dp[n-1][0], dp[n-1][1], ..., dp[n-1][마지막 인덱스] 중에서
print(max(dp[n-1]))
        
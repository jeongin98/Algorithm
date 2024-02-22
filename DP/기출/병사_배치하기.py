# 기출 - 병사_배치하기(백준_18353)

n = int(input())
soldiers = list(map(int, input().split()))
soldiers.reverse() # LIS 알고리즘을 내림차순으로 바꿈

dp = [1] * n

for i in range(1, n):
    for j in range(i):
        if soldiers[j] < soldiers[i]:
            dp[i] = max(dp[i], dp[j]+1)

print(n-max(dp))
https://www.acmicpc.net/problem/1149

### 풀이 날짜

2025-10-31

### 문제 분석 요약
- N개의 집이 일렬로 있다.
- 각 집은 빨강(R), 초록(G), 파랑(B) 중 하나로 칠할 수 있다.
- 단, 인접한 두 집의 색은 같을 수 없다.
- 각 집을 특정 색으로 칠하는 비용이 주어졌을 때, 전체 집을 모두 칠하는 최소 비용을 구하라.

### 알고리즘 설계

#### 필요한 값

- 입력:
    - N(집의 개수)
    - costs : N행 3열의 리스트
``` python
costs[i][0] : i번째 집을 빨강으로 칠하는 비용
costs[i][1] : i번째 집을 초록으로 칠하는 비용
costs[i][2] : i번째 집을 파랑으로 칠하는 비용
```
- 출력: 모든 집을 칠했을 때의 최소 총 비용 (int)

#### 풀이 순서
1. DP 테이블 정의
dp[i][j] = i번째 집을 색 j로 칠했을 때의 최소 누적 비용
(j = 0:R, 1:G, 2:B)

2. 초기값 설정
첫 번째 집은 이전이 없으므로
dp[0] = costs[0]

3. 점화식 (인접 색이 달라야 함)
``` python
dp[i][0] = min(dp[i-1][1], dp[i-1][2]) + costs[i][0]  # i번째 집을 빨강
dp[i][1] = min(dp[i-1][0], dp[i-1][2]) + costs[i][1]  # i번째 집을 초록
dp[i][2] = min(dp[i-1][0], dp[i-1][1]) + costs[i][2]  # i번째 집을 파랑
```
- i번째 집이 특정 색으로 칠해졌다면,
이전 집(i-1)은 그 색이 아니어야 함을 위 식으로 반영한다.

4. 결과 계산
마지막 집(N-1)을 어떤 색으로 칠했든 상관없으므로
``` python
answer = min(dp[N-1][0], dp[N-1][1], dp[N-1][2])
```
## Python (백준 표준 입력 대응)

```python
import sys
input = sys.stdin.readline

N = int(input())
costs = [list(map(int, input().split())) for _ in range(N)]

# dp[i][0] = i번째 집을 빨강으로 칠했을 때의 최소 비용
# dp[i][1] = i번째 집을 초록으로 칠했을 때의 최소 비용
# dp[i][2] = i번째 집을 파랑으로 칠했을 때의 최소 비용
dp = [[0]*3 for _ in range(N)]
dp[0][0], dp[0][1], dp[0][2] = costs[0]

for i in range(1, N):
    dp[i][0] = min(dp[i-1][1], dp[i-1][2]) + costs[i][0]
    dp[i][1] = min(dp[i-1][0], dp[i-1][2]) + costs[i][1]
    dp[i][2] = min(dp[i-1][0], dp[i-1][1]) + costs[i][2]

print(min(dp[N-1][0], dp[N-1][1], dp[N-1][2]))

```

## JavaScript (Node.js, 백준 표준 입력 대응)

```javascript
const fs = require('fs');
const input = fs.readFileSync('/dev/stdin').toString().trim().split('\n');
const N = Number(input[0]);
const costs = input.slice(1).map(line => line.split(' ').map(Number));

const dp = Array.from({ length: N }, () => [0,0,0]);
dp[0][0] = costs[0][0];
dp[0][1] = costs[0][1];
dp[0][2] = costs[0][2];

for (let i = 1; i < N; i++) {
  dp[i][0] = Math.min(dp[i-1][1], dp[i-1][2]) + costs[i][0];
  dp[i][1] = Math.min(dp[i-1][0], dp[i-1][2]) + costs[i][1];
  dp[i][2] = Math.min(dp[i-1][0], dp[i-1][1]) + costs[i][2];
}

const result = Math.min(dp[N-1][0], dp[N-1][1], dp[N-1][2]);
console.log(result);

```

### 시간 복잡도

- O(N)
    - N개의 집을 각각 한 번씩 처리 (각 단계는 상수 시간 연산)
    - 초기화와 최소값 계산 모두 O(1)

### 느낀점 or 기억할 정보
- 이 문제는 전형적인 동적계획법(DP) 문제로,
“현재 상태의 최소 비용이 이전 상태의 선택에 따라 결정된다”는 구조를 갖고 있다.
즉, “이전 집의 색과 달라야 한다”는 제약을 점화식의 최소값 선택으로 자연스럽게 표현했다.
- 세 가지 조건이 모두 이 점화식 안에 포함되어 있다.
``` python
dp[i][color] = min(dp[i-1][다른색]) + cost[i][color]
```
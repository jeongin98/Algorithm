https://www.acmicpc.net/problem/1463

###  풀이 날짜
2025-09-10

###  문제 분석 요약
- 숫자를 1로 만드는데 필요한 최소 연산의 수 출력
- 가능한 연산
  - N → N-1
  - N → N/2 (2로 나누어떨어질 때)
  - N → N/3 (3으로 나누어떨어질 때)

### 알고리즘 설계
#### 필요한 값
- 입력 정수: N
- DP 배열: dp[0..N]
- 의미: dp[i] = 정수 i를 1로 만드는 최소 연산 횟수
  
#### 풀이 순서
1. dp를 길이 N+1로 생성하고 0으로 초기화한다. (dp[1]=0은 자동/명시 둘 다 가능)
2. `i = 2..N`에 대해 다음을 반복한다.
- 기본값으로 dp[i] = dp[i-1] + 1을 설정한다.
  (−1 연산은 항상 가능하므로 기본 후보로 둔다)
- 만약 i % 2 == 0이면 dp[i] = min(dp[i], dp[i//2] + 1)로 갱신한다.
- 만약 i % 3 == 0이면 dp[i] = min(dp[i], dp[i//3] + 1)로 갱신한다.
3. 최종 답은 dp[N]을 출력한다.
  

## Python (표준 입력 대응)
``` python
import sys

n = int(sys.stdin.readline())
dp = [0] * (n + 1)  # dp[1] = 0 포함

for i in range(2, n + 1):
    dp[i] = dp[i - 1] + 1
    if i % 2 == 0:
        dp[i] = min(dp[i], dp[i // 2] + 1)
    if i % 3 == 0:
        dp[i] = min(dp[i], dp[i // 3] + 1)

print(dp[n])

```


## JavaScript (Node.js, 백준 표준 입력 대응)
``` javascript
const fs = require('fs');
const n = Number(fs.readFileSync(0, 'utf8').trim());

const dp = new Array(n + 1).fill(0); // dp[1] = 0

for (let i = 2; i <= n; i++) {
  let best = dp[i - 1] + 1;
  if (i % 2 === 0) best = Math.min(best, dp[i / 2] + 1);
  if (i % 3 === 0) best = Math.min(best, dp[i / 3] + 1);
  dp[i] = best;
}

console.log(dp[n]);
```

<img width="617" height="57" alt="image" src="https://github.com/user-attachments/assets/1e115f80-2f6a-479b-a8a5-65420fee22ba" />



### 시간 복잡도
- O(N)
  - 각 i에 대해 상수 개(최대 3개)의 후보만 비교하므로 선형이다.

### 느낀점 or 기억할 정보
- 깨달은 점
  - dp[i-1]+1(항상 가능)을 기본값으로 두고 /2, /3로 조건부 갱신한다.
  - Greedy가 안 되는 이유 : 현재 단계에서 “좋아 보이는 선택”이 전체 최적해를 보장할 수 없을 때.
    즉, 국소 최적(local optimum)이 전역 최적(global optimum)이 아니다.
    
    → Greedy가 가능한 경우 :
      - 매 순간의 최적 선택이 전체 최적해로 **항상 이어진다는 보장(증명)**이 있을 때.
        - ex 반례로 살펴보기
          예를 들어 N = 10일 때:
          
          **Greedy 방식**
            - 10은 2로 나눠지니까 /2 → 5 (연산 1회)
            - 5는 3으로 안 나눠지니까 -1 → 4 (연산 2회)
            - 4는 2로 나눠지니까 /2 → 2 (연산 3회)
            - 2는 /2 → 1 (연산 4회)
              
              → 총 4번(DP는 3번으로 끝남)
                즉, **국소적으로 좋아 보이는 선택(현재 최적)** 이 전체 최적을 보장하지 못한 것이다.

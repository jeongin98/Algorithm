https://www.acmicpc.net/problem/15650

### 풀이 날짜

2025-10-13

### 문제 분석 요약

- 1부터 N까지 자연수 중 중복 없이 오름차순으로 M개를 고르는 조합을 모두 출력하는 문제.
- 즉, “1~N에서 M개를 순서 없이 선택”하는 조합(Combination) 문제이다.

### 알고리즘 설계

- 아이디어:
  불필요한 경우의 수를 가지치기(pruning)하며 문제를 풀어나간다.
  → DFS(깊이 우선 탐색)를 이용한 백트래킹으로 조합을 생성한다.
  숫자를 하나씩 선택하고, 선택한 숫자보다 큰 수만 다음 단계에서 선택하도록 하여 오름차순을 유지한다.

- 조합 라이브러리를 사용하는 방법도 있다. (Python의 itertools.combinations, JS에서는 재귀로 직접 구현)

#### 필요한 값

- 입력: N(전체 숫자 개수), M(선택할 개수)
- 출력: 오름차순으로 정렬된 모든 M개의 조합

#### 풀이 순서

1. dfs(start) 함수를 정의한다.

- start: 다음 탐색을 시작할 숫자
- 현재까지 선택된 수열은 picked 리스트에 저장

2. 만약 picked 길이 == M이라면 결과 리스트에 추가하고 리턴

3. for i in range(start, N+1) 반복

- 현재 숫자 i를 선택 (picked.append(i))
- dfs(i + 1) 호출 (이후엔 더 큰 수만 탐색)
- picked.pop()으로 원상복구 (backtracking)

4. 모든 탐색이 끝나면 결과 출력

## Python (백준 표준 입력 대응)

```python
import sys
n, m = map(int, sys.stdin.readline().split())

picked = []
result = []

def dfs(start):
    if len(picked) == m:
        result.append(' '.join(map(str, picked)))
        return

    for i in range(start, n + 1):
        picked.append(i)
        dfs(i + 1)
        picked.pop()

dfs(1)
sys.stdout.write('\n'.join(result))
```

## JavaScript (Node.js, 백준 표준 입력 대응)

```javascript
const fs = require("fs");
const [N, M] = fs.readFileSync(0, "utf8").trim().split(/\s+/).map(Number);

const picked = [];
const result = [];

function dfs(start) {
  if (picked.length === M) {
    result.push(picked.join(" "));
    return;
  }

  for (let i = start; i <= N; i++) {
    picked.push(i); // 현재 숫자 선택
    dfs(i + 1); // 다음 숫자는 현재보다 큰 숫자만 선택
    picked.pop(); // 백트래킹(원복)
  }
}

dfs(1);
console.log(result.join("\n"));
```

### 시간 복잡도

- O(C(N,M))
  - 조합을 전부 출력하는 문제이기 때문

### 느낀점 or 기억할 정보

- 처음엔 파이썬 조합만 떠올랐을뿐, 백트래킹을 생각해내지 못 했다. 백트래킹은 코테에서 자주 나오기 때문에 백트래킹의 특성을 잘 이해해두고 이용할 것!
- 백트래킹은 **“되돌아가는 탐색”**으로, 조건에 맞지 않거나 불필요한 경로는 가지치기(pruning) 하여 효율적으로 탐색한다.
- 조합 문제에서는 start 인덱스 조절만으로 (중복 없이) 오름차순 조합을 만들 수 있다. → 방문 여부를 저장하는 visited 배열을 따로 만들어서 체크하지 않아도 되는 이유(애초에 오름차순 선택으로 중복이 원천 차단)
- 단순 반복(ex. for문 여러겹)보다 훨씬 구조적인 탐색을 제공한다.

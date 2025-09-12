https://www.acmicpc.net/problem/1012

###  풀이 날짜
2025-09-12

###  문제 분석 요약
- 여러 테스트케이스에 대해, 가로 M × 세로 N 격자에 배추가 심어진 위치가 K개 주어지고,
- 상·하·좌·우로 인접한 배추들은 하나의 연결된 배추 군집(=연결요소) 이며,
- 각 테스트케이스마다 서로 다른 군집의 개수(=필요한 지렁이 수) 를 출력한다.

### 알고리즘 설계
#### 필요한 값
- 입력:
  - T (테스트 케이스 수)
  - 각 테스트케이스마다: M N K
  - 이어서 K줄: (x, y) — 가로 x, 세로 y 좌표(0 ≤ x < M, 0 ≤ y < N)
- 격자: N × M (행 N=세로, 열 M=가로)
- 인접 기준: 상 하 좌 우
- 목표 : 배추가 심어진 칸(1)들을 BFS/DFS로 묶어 연결요소의 개수를 구한다.
  
#### 풀이 순서
1. 테스트 케이스마다 N × M 격자를 0으로 초기화하고, 입력된 (x, y)에 대해 grid[y][x] = 1로 표시
2. visited 배열(or 격자값을 0으로 지우기)로 방문여부를 관리
3 모든 칸을 순회하며, 아직 방문하지 않은 배추 칸(=1) 을 발견할 때마다 BFS/DFS를 시작해 해당 군집을 전부 방문 처리
- 시작할 때 군집 수 += 1
- 큐/스택에서 꺼낸 좌표의 4방향을 확인: 격자 내 & 배추(1) & 미방문이면 방문 처리 후 큐/스택에 넣기
4. 순회가 끝나면 누적된 군집 수를 출력한다.

## Python (BFS, 표준 입력 대응)
``` python
import sys
from collections import deque

input = sys.stdin.readline

T = int(input().strip())
dirs = [(1,0), (-1,0), (0,1), (0,-1)]

for _ in range(T):
    M, N, K = map(int, input().split())  # M: 가로(열), N: 세로(행)
    grid = [[0]*M for _ in range(N)]
    for _ in range(K):
        x, y = map(int, input().split())
        grid[y][x] = 1

    def bfs(sr, sc):
        q = deque([(sr, sc)])
        grid[sr][sc] = 0  # 방문 처리(지우기)
        while q:
            r, c = q.popleft()
            for dc, dr in dirs:  # (x증가, y증가) 순으로 저장했지만 아래서 (c+dc, r+dr)로 사용
                nc, nr = c + dc, r + dr
                if 0 <= nr < N and 0 <= nc < M and grid[nr][nc] == 1:
                    grid[nr][nc] = 0
                    q.append((nr, nc))

    worms = 0
    for r in range(N):
        for c in range(M):
            if grid[r][c] == 1:
                bfs(r, c)
                worms += 1
    print(worms)


```


## JavaScript (Node.js, 백준 표준 입력 대응)
``` javascript
// Node.js (ECMAScript 2021)
const fs = require('fs');

const tokens = fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(Number);
let idx = 0;

const T = tokens[idx++];

// 4방향
const dx = [1, -1, 0, 0];
const dy = [0, 0, 1, -1];

let outputs = [];

for (let t = 0; t < T; t++) {
  const M = tokens[idx++]; // 가로(열)
  const N = tokens[idx++]; // 세로(행)
  const K = tokens[idx++];

  // grid[y][x]
  const grid = Array.from({ length: N }, () => Array(M).fill(0));
  for (let i = 0; i < K; i++) {
    const x = tokens[idx++], y = tokens[idx++];
    grid[y][x] = 1;
  }

  const bfs = (sr, sc) => {
    const q = [];
    let head = 0;
    q.push([sr, sc]);
    grid[sr][sc] = 0; // 방문 처리

    while (head < q.length) {
      const [r, c] = q[head++];
      for (let dir = 0; dir < 4; dir++) {
        const nc = c + dx[dir];
        const nr = r + dy[dir];
        if (nr >= 0 && nr < N && nc >= 0 && nc < M && grid[nr][nc] === 1) {
          grid[nr][nc] = 0;
          q.push([nr, nc]);
        }
      }
    }
  };

  let worms = 0;
  for (let r = 0; r < N; r++) {
    for (let c = 0; c < M; c++) {
      if (grid[r][c] === 1) {
        bfs(r, c);
        worms++;
      }
    }
  }
  outputs.push(String(worms));
}

console.log(outputs.join('\n'));
```
<img width="626" height="58" alt="image" src="https://github.com/user-attachments/assets/41b4111b-8450-4c3d-b4cd-4cbacad6a66f" />



### 시간 복잡도
- O(N×M)
  - 각 칸/혹은 각 배추 좌표를 최대 한 번씩만 방문 
  - 각 칸마다 4방향만 확인 → 상수 배수

### 느낀점 or 기억할 정보
- 연결요소 개수 = 시작점 개수(미방문 배추 칸에서 BFS/DFS를 시작한 횟수이다.)
- 입력이 여러 테스트케이스라는 점, 좌표가 (x, y) = (열, 행) 순서라는 점에 주의할 것
- 파이썬은 재귀 DFS는 제한에 걸릴 수 있으니 BFS(deque) 가 안정적이다.

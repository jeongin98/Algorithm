https://www.acmicpc.net/problem/18809

### 풀이 날짜

2025-10-27

### 문제 분석 요약
- 격자에 0(호수), 1(일반 땅), 2(비옥한 땅)이 있음.

- 비옥한 땅(2) 에만 배양액(초록 G개, 빨강 R개)을 놓을 수 있음.

- 초록/빨강은 1분마다 4방향으로 (0,1,2) 중 0이 아닌 칸으로 확산.

- 어떤 칸에 같은 시각에 초록과 빨강이 동시에 도착하면 꽃이 피고, 그 칸에서 더 이상 확산하지 않음.

- 배치(초록/빨강 위치 선택)와 확산을 모두 고려하여 꽃의 총 개수 최대값을 구하는 문제.

핵심 난이도 포인트

- 비옥한 땅의 개수 K(≤ 10 정도)에서 조합적으로 G+R개를 뽑고, 그 중 G개를 초록으로 선택 → 경우의 수 시뮬레이션.

- 시뮬레이션은 동시성 보장 BFS로 “같은 시간 도착 → 꽃” 로직을 정확하게 구현해야 함.
### 알고리즘 설계

#### 필요한 값

- 입력:
    - N, M (격자 크기), G, R (초록/빨강 개수)
    - N×M 격자(0/1/2)
- 출력: 만들 수 있는 꽃의 최대 개수

#### 풀이 순서
1. 비옥한 땅 1위치 수집
지도에서 값이 2인 칸(비옥한 땅)의 좌표를 모두 저장한다.
이 좌표들만이 배양액을 놓을 수 있는 후보지가 된다.

2. 배양액 배치의 모든 조합 탐색

비옥한 땅의 개수를 K라고 했을 때,
이 중 초록 G개, 빨강 R개를 배치해야 한다.

즉, 가능한 모든 배치를 전부 탐색해야 한다.

구현 방식은 보통 두 단계로 나눈다:

먼저 비옥한 땅 중 G+R개를 선택한다.

그중 일부를 초록(G개)으로, 나머지를 빨강(R개)으로 지정한다.

이 방법을 통해 초록과 빨강의 모든 배치를 빠짐없이 고려할 수 있다.

3. BFS(동시 확산) 시뮬레이션

초록과 빨강이 동시에 확산하도록 큐에 모두 넣고 진행한다.

각 칸에는 두 개의 도착 시간(timeG, timeR)을 따로 기록한다.

초록과 빨강이 같은 시간에 도착하면 그 칸은 꽃이 되고, 이후에는 확산이 멈춘다.

초록 또는 빨강 중 한쪽만 먼저 도착한 경우에는 도착한 색으로 확산을 계속한다.

호수(0)는 퍼질 수 없으며, 이미 꽃이 핀 칸은 다시 방문하지 않는다.

4. 꽃 개수 계산 및 최대값 갱신

각 배치 조합별로 BFS 결과를 계산한 뒤,
꽃의 개수를 세어 최대값을 갱신한다.

5. 최대 꽃 개수를 출력

## Python (백준 표준 입력 대응)

```python
import sys
from itertools import combinations
from collections import deque

input = sys.stdin.readline

N, M, G, R = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]

fertile = [(i, j) for i in range(N) for j in range(M) if board[i][j] == 2]
K = len(fertile)

dirs = [(-1,0),(1,0),(0,-1),(0,1)]

def simulate(greens, reds):
    timeG = [[-1]*M for _ in range(N)]
    timeR = [[-1]*M for _ in range(N)]
    flower = [[False]*M for _ in range(N)]

    q = deque()
    for (r, c) in greens:
        timeG[r][c] = 0
        q.append((r, c, 0, 'G'))
    for (r, c) in reds:
        timeR[r][c] = 0
        q.append((r, c, 0, 'R'))

    flowers = 0

    while q:
        r, c, t, col = q.popleft()
        if flower[r][c]:
            continue  # 꽃 칸에서는 확산 중지

        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if nr < 0 or nr >= N or nc < 0 or nc >= M:
                continue
            if board[nr][nc] == 0:
                continue

            if col == 'G':
                if timeG[nr][nc] != -1 or flower[nr][nc]:
                    continue
                # 빨강이 이미 왔는지 확인
                if timeR[nr][nc] == -1:
                    timeG[nr][nc] = t+1
                    q.append((nr, nc, t+1, 'G'))
                else:
                    # 빨강 도착 시간이 같으면 꽃
                    if timeR[nr][nc] == t+1 and not flower[nr][nc]:
                        flower[nr][nc] = True
                        flowers += 1
            else:  # 'R'
                if timeR[nr][nc] != -1 or flower[nr][nc]:
                    continue
                if timeG[nr][nc] == -1:
                    timeR[nr][nc] = t+1
                    q.append((nr, nc, t+1, 'R'))
                else:
                    if timeG[nr][nc] == t+1 and not flower[nr][nc]:
                        flower[nr][nc] = True
                        flowers += 1

    return flowers

ans = 0
# (1) G+R개 선택
for picked in combinations(range(K), G+R):
    picked_list = [fertile[i] for i in picked]
    # (2) 이 중 G개를 초록으로
    for greens_idx in combinations(range(G+R), G):
        greens = [picked_list[i] for i in greens_idx]
        reds = [picked_list[i] for i in range(G+R) if i not in greens_idx]
        ans = max(ans, simulate(greens, reds))

print(ans)

```

## JavaScript (Node.js, 백준 표준 입력 대응)

```javascript

const fs = require('fs');
const input = fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(Number);
let idx = 0;

const N = input[idx++], M = input[idx++], G = input[idx++], R = input[idx++];
const board = Array.from({ length: N }, () => Array.from({ length: M }, () => input[idx++]));

// 비옥한 땅(2) 좌표 수집
const fertile = [];
for (let i = 0; i < N; i++) {
  for (let j = 0; j < M; j++) {
    if (board[i][j] === 2) fertile.push([i, j]);
  }
}
const K = fertile.length;
const dirs = [[-1,0],[1,0],[0,-1],[0,1]];

/**
 * 동시 다원 BFS 시뮬레이션
 * @param {Array<[number,number]>} greens - 초록 시작 좌표 배열
 * @param {Array<[number,number]>} reds   - 빨강 시작 좌표 배열
 * @returns {number} 꽃 개수
 */
function simulate(greens, reds) {
  const timeG = Array.from({ length: N }, () => Array(M).fill(-1));
  const timeR = Array.from({ length: N }, () => Array(M).fill(-1));
  const flower = Array.from({ length: N }, () => Array(M).fill(false));

  // 하나의 큐에 (r, c, t, col)로 같이 넣어도 되지만
  // 여기서는 배열+포인터로 간단 큐를 구현
  const q = [];
  let head = 0;

  for (const [r, c] of greens) {
    timeG[r][c] = 0;
    q.push([r, c, 0, 0]); // col: 0=G, 1=R
  }
  for (const [r, c] of reds) {
    timeR[r][c] = 0;
    q.push([r, c, 0, 1]);
  }

  let flowers = 0;

  while (head < q.length) {
    const [r, c, t, col] = q[head++];
    if (flower[r][c]) continue; // 꽃 칸에서는 확산 중지

    for (const [dr, dc] of dirs) {
      const nr = r + dr, nc = c + dc;
      if (nr < 0 || nr >= N || nc < 0 || nc >= M) continue;
      if (board[nr][nc] === 0) continue; // 호수로 이동 불가

      if (col === 0) { // 초록 확산
        if (timeG[nr][nc] !== -1 || flower[nr][nc]) continue;

        if (timeR[nr][nc] === -1) {
          // 빨강이 아직 안 왔으면 초록 먼저 도착
          timeG[nr][nc] = t + 1;
          q.push([nr, nc, t + 1, 0]);
        } else {
          // 빨강 도착시간과 같은 시각이면 꽃
          if (timeR[nr][nc] === t + 1 && !flower[nr][nc]) {
            flower[nr][nc] = true;
            flowers += 1;
          }
          // 빨강이 더 이르거나 늦으면 초록은 퍼지지 않음(이 타이밍에만 꽃 가능)
        }
      } else { // 빨강 확산
        if (timeR[nr][nc] !== -1 || flower[nr][nc]) continue;

        if (timeG[nr][nc] === -1) {
          timeR[nr][nc] = t + 1;
          q.push([nr, nc, t + 1, 1]);
        } else {
          if (timeG[nr][nc] === t + 1 && !flower[nr][nc]) {
            flower[nr][nc] = true;
            flowers += 1;
          }
        }
      }
    }
  }
  return flowers;
}

/**
 * 조합 생성기: n개 중 r개 인덱스를 뽑는 조합을 배열로 반환
 */
function combinationsIdx(n, r) {
  const res = [];
  const comb = [];
  function dfs(start, k) {
    if (k === r) {
      res.push(comb.slice());
      return;
    }
    for (let i = start; i < n; i++) {
      comb.push(i);
      dfs(i + 1, k + 1);
      comb.pop();
    }
  }
  dfs(0, r);
  return res;
}

let answer = 0;

// (1) K개 중 G+R개 선택
const pickGR = combinationsIdx(K, G + R);
for (const picked of pickGR) {
  // 실제 좌표 리스트
  const slots = picked.map(i => fertile[i]);
  // (2) 이 중 G개를 초록으로 선택
  const greensChoices = combinationsIdx(G + R, G);
  for (const gIdxs of greensChoices) {
    const green = [];
    const red = [];
    const gSet = new Set(gIdxs);
    for (let i = 0; i < G + R; i++) {
      if (gSet.has(i)) green.push(slots[i]);
      else red.push(slots[i]);
    }
    const flowers = simulate(green, red);
    if (flowers > answer) answer = flowers;
  }
}

console.log(answer.toString());

```

### 시간 복잡도

- O(조합 수 × N × M)
 - 배양액 배치 조합 생성: O(조합 수)
    → 비옥한 땅의 개수가 K일 때, 초록 G개와 빨강 R개를 놓는 모든 배치를 완전탐색
    → (K가 최대 10 정도로 작기 때문에 충분히 계산 가능)

- 각 배치별 BFS 시뮬레이션: O(N × M)
    → 격자 전체를 한 번씩 탐색하며 확산 진행

- 전체 수행: 모든 배치에 대해 BFS를 반복하므로 O(조합 수 × N × M)

### 느낀점 or 기억할 정보
- 이 문제의 핵심은 “배양액 배치의 모든 조합을 탐색해야 한다”는 점이다.
어떤 칸에 초록을, 어떤 칸에 빨강을 두느냐에 따라 꽃이 피는 위치와 개수가 완전히 달라진다.

- 조합을 구하는 방식은 “먼저 G+R개를 뽑고 그중 G개를 초록으로 정한다” 혹은
“먼저 초록 G개를 고르고, 남은 곳 중 R개를 빨강으로 정한다” 두 가지 방법이 있으며
두 방식 모두 같은 결과를 얻을 수 있다.

- BFS에서는 반드시 “동시에 도착한 칸만 꽃으로 처리”하고,
“꽃이 된 칸은 확산을 멈춘다”는 규칙을 정확히 지켜야 한다.

- 겉보기엔 구현이 복잡해 보이지만, 정석적인 조합 탐색 + BFS 구현 패턴만 정확히 적용하면
문제를 안정적으로 해결할 수 있다.

- 실제로 입력 크기가 작아서 시간 제한이 넉넉하기 때문에,
완전 탐색을 수행해도 충분히 통과할 수 있다.

- 체감 난이도는 높지만 “탐색과 시뮬레이션을 동시에 다루는 좋은 연습문제”이며,
정확한 동시 도착 판정 로직과 조합 구현 능력을 함께 점검할 수 있다.
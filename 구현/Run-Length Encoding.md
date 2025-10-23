https://www.acmicpc.net/problem/6538

### 풀이 날짜

2025-10-23

### 문제 분석 요약
- - 많은 조건과 핵심 트릭이 있어서 주의해서 풀어야함.

- 주어진 문자열을 특수 규칙의 RLE로 라인 단위 인코딩한다.

- 반복(run): 동일 문자가 2~9개 연속 → "{길이}{문자}"
10개 이상이면 9개 단위로 끊어 출력 후 나머지를 동일 규칙 적용.
(예: aaaaaaaaaa(10개) → 9a + 남은 1개는 literal → 1a1)

- 비반복(literal): 연속 반복이 전혀 없는 구간은 "1" + (구간) + "1"로 감싼다.
이때 구간 내부의 '1'은 11로 이스케이프한다.

- 중요: '1'이 연속으로 2개 이상이면 literal이 아니라 반복(run) 으로 처리해야 한다. (예: 1111 → 41)

- 개행(\n)은 인코딩하지 않고 그대로 출력한다 (라인별 독립 처리).

### 알고리즘 설계

#### 필요한 값

- 입력: 여러 줄의 문자열(영문자 대소문, 숫자, 공백, 구두점). 각 줄은 \n으로 끝남.
- 출력: 각 줄 본문을 규칙대로 인코딩한 뒤, 마지막에 원래 개행을 그대로 출력.

#### 풀이 순서
1. 표준 입력을 라인 단위로 읽는다. 각 줄에서 마지막 개행만 제거하고 본문만 인코딩한다.

2. 본문을 왼쪽부터 훑으면서:
    - 현재 문자와 동일한 문자가 몇 개 연속되는지(run_len) 센다.
    - run_len >= 2이면 반복 구간(run):
        - 9개씩 끊어 "{k}{문자}"를 출력 (k = min(run_len, 9) 반복).
        - 남은 1개가 있다면(즉, 전체가 10, 19, …처럼 9의 배수+1일 때)
        그 1개는 literal 규칙으로 1{문자}1 출력. (예: 9a + 1a1)
    - run_len == 1이면 비반복 누적(literal 버퍼):
        - 다음에 반복(run)을 만나거나 문자열이 끝날 때까지 모은 뒤,
        - "1" + (이스케이프된 본문: '1'→'11') + "1"로 출력.
3. 줄마다 인코딩된 결과를 출력하고, 개행은 그대로 붙여준다.

## Python (백준 표준 입력 대응)

```python
import sys

def encode_line(line):
    """
    한 줄의 문자열을 run-length encoding 방식으로 인코딩하는 함수
    """
    # 빈 문자열이면 빈 문자열 반환
    if not line:
        return ""
    
    # 인코딩 결과를 저장할 리스트
    result = []
    
    # 현재 처리 중인 문자열의 인덱스
    i = 0
    
    # 문자열의 끝까지 반복
    while i < len(line):
        # === STEP 1: 현재 위치에서 연속된 동일 문자의 개수를 센다 ===
        count = 1  # 현재 문자 자체를 포함하므로 1부터 시작
        
        # 다음 문자가 존재하고, 현재 문자와 같은 동안 계속 카운트 증가
        while i + count < len(line) and line[i] == line[i + count]:
            count += 1
        
        # === STEP 2: 연속된 문자가 2개 이상인 경우 (반복 문자 처리) ===
        if count >= 2:
            # 반복되는 문자를 저장
            char = line[i]
            
            # 남은 반복 횟수를 저장
            remaining = count
            
            # 남은 반복 횟수가 2개 이상인 동안 반복 (1개는 단일 문자로 처리)
            while remaining >= 2:
                # 한 번에 최대 9개까지만 인코딩 가능
                encode_count = min(remaining, 9)
                
                # 결과에 "개수 + 문자" 형태로 추가 (예: "9a")
                result.append(str(encode_count))
                result.append(char)
                
                # 처리한 개수만큼 remaining에서 빼기
                remaining -= encode_count
            
            # === STEP 2-1: 마지막 남은 개수가 1개인 경우 ===
            # 예: 10개의 'a' -> 9개 처리 후 1개 남음
            # 이 1개는 "반복 문자"가 아니라 "단일 문자"로 처리해야 함
            if remaining == 1:
                # 비반복 시퀀스 시작 표시
                result.append('1')
                
                # 만약 문자가 '1'이면 '11'로 이스케이프
                if char == '1':
                    result.append('11')
                else:
                    result.append(char)
                
                # 비반복 시퀀스 종료 표시
                result.append('1')
            
            # 처리한 모든 문자를 건너뛰기 위해 인덱스 이동
            i += count
        
        # === STEP 3: 연속된 문자가 1개인 경우 (비반복 문자 처리) ===
        else:
            # 비반복 문자들을 모을 리스트
            seq = []
            
            # 반복 문자가 나올 때까지 비반복 문자를 계속 수집
            while i < len(line):
                # 현재 위치에서 다음에 반복 문자가 나오는지 확인
                next_count = 1
                
                # 현재 위치부터 연속된 동일 문자 개수 확인
                while i + next_count < len(line) and line[i] == line[i + next_count]:
                    next_count += 1
                
                # 2개 이상 반복되는 문자를 발견하면 루프 종료
                # (반복 문자는 별도로 처리해야 하므로)
                if next_count >= 2:
                    break
                
                # 현재 문자를 비반복 시퀀스에 추가
                seq.append(line[i])
                
                # 다음 문자로 이동
                i += 1
            
            # === STEP 3-1: 수집한 비반복 시퀀스를 인코딩 ===
            if seq:
                # 비반복 시퀀스 시작 표시 '1'
                result.append('1')
                
                # 시퀀스의 각 문자를 처리
                for ch in seq:
                    # 문자가 '1'이면 '11'로 이스케이프 처리
                    # (그래야 디코딩할 때 구분 가능)
                    if ch == '1':
                        result.append('11')
                    else:
                        result.append(ch)
                
                # 비반복 시퀀스 종료 표시 '1'
                result.append('1')
    
    # 리스트에 저장된 모든 문자를 하나의 문자열로 합쳐서 반환
    return ''.join(result)

# 표준 입력에서 한 줄씩 읽어서 처리
for line in sys.stdin:
    # 줄 끝의 개행 문자(\n)를 제거
    line = line.rstrip('\n')
    
    # 인코딩 결과를 출력
    print(encode_line(line))
```

## JavaScript (Node.js, 백준 표준 입력 대응)

```javascript
// BOJ 6538 - Run-Length Encoding (변형 규칙)
// 실행: Node.js (백준 표준 입력/출력)

const fs = require('fs');

// 한 줄(본문) 인코딩 함수
function encodeLine(s) {
  const out = [];        // 결과 조각 누적 (마지막에 join)
  const n = s.length;
  let i = 0;

  let literal = [];      // 반복이 전혀 없는 구간을 임시로 모아두는 버퍼

  while (i < n) {
    const ch = s[i];

    // 현재 문자와 동일한 문자가 몇 개 연속되는지 run 길이 측정
    let j = i + 1;
    while (j < n && s[j] === ch) j++;
    const runLen = j - i;

    if (runLen >= 2) {
      // 반복(run) 구간에 진입했으므로, 먼저 누적된 literal을 비워 출력
      if (literal.length > 0) {
        // literal 내부의 '1'은 '11'로 이스케이프
        const block = literal.join('').replace(/1/g, '11');
        out.push('1' + block + '1');
        literal = [];
      }

      // 9개 단위로 run을 끊어 출력
      let remaining = runLen;
      while (remaining >= 2) {
        const k = Math.min(remaining, 9); // 최대 9
        out.push(String(k) + ch);
        remaining -= k;
      }

      // ★ 트릭 포인트: 만약 1개가 남았다면 literal로 처리해야 정답
      if (remaining === 1) {
        // ch가 '1'이면 literal 내부 이스케이프 규칙에 따라 '11'이 되어야 함
        out.push('1', ch === '1' ? '11' : ch, '1');
      }

      i = j; // run 끝으로 점프
    } else {
      // run_len === 1 → literal 누적 모드
      literal.push(ch);
      i = j; // 다음 문자로
      // (다음 루프에서 run을 만나거나 끝나면 위에서 literal을 비워 출력)
    }
  }

  // 문자열 끝에 도달했는데 literal이 남았으면 마저 출력
  if (literal.length > 0) {
    const block = literal.join('').replace(/1/g, '11');
    out.push('1' + block + '1');
  }

  return out.join('');
}

(function main() {
  const data = fs.readFileSync(0, 'utf8');        // 표준 입력 전체
  const lines = data.split('\n');                  // 개행 기준 분해
  const nlCount = (data.match(/\n/g) || []).length; // 원본 개행 개수(그대로 복원용)

  for (let idx = 0; idx < lines.length; idx++) {
    const body = lines[idx];                      // 개행 제외 본문
    const encoded = encodeLine(body);
    if (idx < nlCount) {
      // 원래 개행이 있었던 라인 수만큼만 개행을 출력
      process.stdout.write(encoded + '\n');
    } else {
      // 입력이 개행 없이 끝났다면 마지막 라인은 개행 없이 출력
      process.stdout.write(encoded);
    }
  }
})();

```

### 시간 복잡도

- O(N) (N = 라인 길이)
    - JS/Python 모두 result 결과 누적을 리스트/배열.append()로 모았다가 → O(1)
    - 마지막에 ''.join(result) 하는 건 → O(n)

### 느낀점 or 기억할 정보
- 핵심 트릭: 10개 a는 9a + 1a1이다. 남은 1개는 literal로 처리해야 한다.
    ex. 10개의 a가 있을 때 
    - "9a" + "1a1" ✅ 
    - "9a" + "1a" ❌ (잘못!) 

- 성능 팁(문자열 결합):
    - 문자열 "1" + "ch" + "1" 과 같은 방식으로 반복은 O(n²) 으로 비효율적
    - **배열/리스트에 append 후 마지막에 join**은 O(n) → 코딩테스트 표준 패턴.

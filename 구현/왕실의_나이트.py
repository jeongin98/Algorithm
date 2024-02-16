# 실전 - 왕실의 나이트(정렬)
# <구현 - 상하좌우> 문제와 비슷

# 현재 나이트 위치 입력받기
input_data = input()
# ord 문자를 숫자로 바꾸나?
row = int(input_data[1])
column = int(ord(input_data[0])) - int(ord('a')) + 1

# ()와 []의 차이?
# 나이트가 이동할 수 있는 8가지 방향
steps = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

result = 0
for step in steps:
    next_row = row + step[1]
    next_column = column + step[0]
    # 해당 위치로 이동 가능하다면 카운트 증가
    if next_row >= 1 and next_row <= 8 and next_column >= 1 and next_column <= 8:
        result += 1

print(result)


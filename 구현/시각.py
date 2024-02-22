# 기출- 시각
# 매 시각을 문자열로 바꾸어 문자열에 '3'이 표함되어있는지 확인
# 03시 20분 35초라면, '032035'로 만들기

h = int(input())

count= 0 
for i in range(h+1):
    for j in range(60):
        for k in range(60):
            if '3' in str(i) + str(j) + str(k):
                count += 1

print(count)


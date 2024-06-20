# 층 수 입력
value = int(input("층 수를 입력하세요: "))

# 입력한 층 수의 피라미드 출력
for i in range(1, int(value) + 1):
    print(' ' * (int(value) - i) + '*' * (2 * i - 1))
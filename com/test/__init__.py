import tensorflow as tf
import sys
a,b = 0,1

while b<10:
    print(b,end=",")
    a,b=b,a+b


if a == 1:
    print(a)
else:
    print(100000)

for i in range(10):
    print(i)

list = [1, 2, 3, 4]
it = iter(list)  # 创建迭代器对象

# while True:
#     try:
#         print(next(it))
#     except StopIteration:
#         sys.exit()


def fibonacci(n):  # 生成器函数 - 斐波那契
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n):
            return
        yield a
        a, b = b, a + b
        counter += 1


f = fibonacci(10)  # f 是一个迭代器，由生成器返回生成

# while True:
#     try:
#         print(next(f), end=" ")
#     except StopIteration:
#         sys.exit()

# 可写函数说明
sum = lambda arg1, arg2: arg1 + arg2;

# 调用sum函数
print("相加后的值为 : ", sum(10, 20))
print("相加后的值为 : ", sum(20, 20))
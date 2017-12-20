# -*- coding: utf-8 -*-
import math
import cmath
import keyword
import sys

# print("heelo")
# x = input("input some char:")
# print(x)

print(int(math.floor(32.9)))
math.floor(32.9)
# math.sqrt(-1)
print(cmath.sqrt(-1))


print(repr("test HH"))
print(str("test HH"))
a = 11
print("a=",a)

print(keyword.kwlist)

sys.stdout.write("test \n")


print(isinstance(a,int))

class A:
    pass

class B(A):
    pass

print(isinstance(A(),A))
print(type(A()) == A)
print(isinstance(B(),A))
print(type(B()) == A)


list = [1,2,3,4,5,6,7,8,9,"222"]


tinylist = ["111","222"]
print(list)
print(tinylist)


print({x:x**2 for x in (2,4,6,7)})
vec =[1,2,3,4]
list1 = [[x, x**2] for x in vec]
print(list1)
print(list1[1][1])


print(round(1/2,2))

print([str(round(355/113, i)) for i in range(1, 6)])



def area(width,height):
    return width * height;

print(area(10,11))
# input("press <Enter>")
import sys
import math as mth

a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])

d = b*b - 4*a*c

if (d > 0) and (a != 0):
    x_1 = ((-1)*b + mth.sqrt(d))/(2*a)
    print(int(x_1))
    x_2 = ((-1)*b - mth.sqrt(d))/(2*a)
    print(int(x_2))

if (d == 0) and (a != 0):
    x_1 = (-1)*b/(2*a)
    print(int(x_1))

if (a == 0) and (b != 0):
    x_1 = (-1)*(c/b)
    print(int(x_1))

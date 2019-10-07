import sys

digit_string = sys.argv[1]

sum = 0
for i in range(len(digit_string)):
    sum = sum + int(digit_string[i])

print(sum)

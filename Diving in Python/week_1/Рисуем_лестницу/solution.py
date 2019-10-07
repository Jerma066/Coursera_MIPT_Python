import sys
num_steps = int(sys.argv[1])

for i in range(num_steps):
    k = i + 1
    str = (' ')*(num_steps - k) + '#'*k
    print(str)

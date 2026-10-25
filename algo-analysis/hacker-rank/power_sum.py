#
# Complete the 'powerSum' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER X
#  2. INTEGER N
#


def powerSum(X, N, i=1):
    if X == 0:
        return 1
    power = i**N
    if power > X:
        return 0

    return powerSum(X - power, N, i + 1) + powerSum(X, N, i + 1)

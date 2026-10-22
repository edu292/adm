#
# Complete the 'rotateLeft' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER d
#  2. INTEGER_ARRAY arr
#


def rotateLeft(d: int, arr: list):
    length = len(arr)
    shift = d % length
    if shift == 0:
        return arr

    new_head_index = shift
    return arr[new_head_index:] + arr[:new_head_index]

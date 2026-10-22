#
# Complete the 'hackerlandRadioTransmitters' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY x
#  2. INTEGER k
#


def hackerlandRadioTransmitters(addresses: list[int], radio_range: int) -> int:
    addresses.sort()
    antenas = 0
    i = 0
    n = len(addresses)
    while i < n:
        antenas += 1
        right_limit = addresses[i] + radio_range
        while i < n and addresses[i] <= right_limit:
            i += 1
        antena = addresses[i - 1]
        while i < n and addresses[i] <= antena + radio_range:
            i += 1

    return antenas


print(hackerlandRadioTransmitters([7, 2, 4, 6, 5, 9, 12, 11], 2))

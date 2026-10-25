from itertools import zip_longest


def get_carry_count(nums: list[str]) -> int:
    carry_count = 0
    carry = 0
    for digits in zip_longest(*(s[::-1] for s in nums), fillvalue="0"):
        s = sum(int(digit) for digit in digits) + carry
        carry = s // 10
        if carry:
            carry_count += 1

    while carry >= 10:
        carry_count += 1
        carry //= 10

    return carry_count


def main():
    pairs = []
    while (pair := [num for num in input().split()]) != ["0", "0"]:
        pairs.append(pair)

    for pair in pairs:
        carry_count = get_carry_count(pair)
        print(f"{carry_count or 'No'} carry operation{'s' if carry_count else ''}.")


if __name__ == "__main__":
    main()

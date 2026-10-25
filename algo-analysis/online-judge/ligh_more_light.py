import math


def is_bulb_on_iterative(n: int) -> bool:
    bulb_on = False
    for i in range(1, n + 1):
        if n % i == 0:
            bulb_on = not bulb_on

    return bulb_on


def is_bulb_on(n: int) -> bool:
    r = math.isqrt(n)
    return r * r == n


def main():
    bulb_counts = []
    while (bulb_count := int(input())) != 0:
        bulb_counts.append(bulb_count)

    for bulb_count in bulb_counts:
        bulb_on = is_bulb_on(bulb_count)
        print("yes" if bulb_on else "no")


if __name__ == "__main__":
    main()

def collatz(n: int) -> int:
    if n == 1:
        return 1

    if n % 2 == 1:
        return 1 + collatz(3 * n + 1)
    return 1 + collatz(n // 2)


def solve_3n1(i, j):
    if i < j:
        start = i
        end = j
    else:
        start = j
        end = i

    max_cycle_length = 0
    for n in range(start, end + 1):
        cycle_length = collatz(n)
        max_cycle_length = max(max_cycle_length, cycle_length)

    return max_cycle_length


def main():
    results: list[str] = []

    while True:
        limits = (int(limit) for limit in input().split())
        if not limits:
            break

        start, end = limits
        max_cycle_length = solve_3n1(start, end)
        results.append(f"{start} {end} {max_cycle_length}")

    for result in results:
        print(result)


if __name__ == "__main__":
    main()

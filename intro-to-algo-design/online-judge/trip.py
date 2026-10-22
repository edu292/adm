def solve_trip(expenses_cents: list[int]):
    member_count = len(expenses_cents)
    total_cents = sum(expenses_cents)
    base_share_cents = total_cents // member_count
    remaining_base_shares = member_count - total_cents % member_count

    expenses_cents.sort()

    transferred_cents = 0
    for expense_cents in expenses_cents:
        if expense_cents > base_share_cents:
            break

        if remaining_base_shares:
            remaining_base_shares -= 1
        else:
            transferred_cents += 1

        transferred_cents += base_share_cents - expense_cents

    return transferred_cents


def main():
    trip_transfers_cents = []

    while True:
        student_count = int(input())
        if student_count == 0:
            break

        expenses_cents = []
        for _ in range(student_count):
            expense_cents = round(float(input()) * 100)
            expenses_cents.append(expense_cents)

        transferred_cents = solve_trip(expense_cents)
        trip_transfers_cents.append(transferred_cents)

    for transferred_cents in trip_transfers_cents:
        print(f"${transferred_cents / 100:.2f}")


if __name__ == "__main__":
    main()

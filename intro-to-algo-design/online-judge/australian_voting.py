def solve_voting(candidates: list[str], ballots: list[list[int]]) -> list[str]:
    candidate_count: int = len(candidates)
    majority: int = len(ballots) // 2
    eliminated_candidate_ids: set[int] = set()

    while True:
        candidate_to_ballot_ids: list[list[int]] = [[] for _ in range(candidate_count)]
        for ballot_id, ballot in enumerate(ballots):
            for candidate_number in ballot:
                candidate_id = candidate_number - 1
                if candidate_id in eliminated_candidate_ids:
                    continue

                candidate_to_ballot_ids[candidate_id].append(ballot_id)
                break

        highest_vote_count: int = 0
        top_candidate_ids: list[int] = []
        lowest_vote_count: int = len(ballots)
        bottom_candidate_ids: list[int] = []

        for candidate_id, assigned_ballot_ids in enumerate(candidate_to_ballot_ids):
            if candidate_id in eliminated_candidate_ids:
                continue

            vote_count = len(assigned_ballot_ids)

            if vote_count >= highest_vote_count:
                if vote_count > highest_vote_count:
                    highest_vote_count = vote_count
                    top_candidate_ids.clear()

                top_candidate_ids.append(candidate_id)

            if vote_count <= lowest_vote_count:
                if vote_count < lowest_vote_count:
                    lowest_vote_count = vote_count
                    bottom_candidate_ids.clear()

                bottom_candidate_ids.append(candidate_id)

        active_candidate_count = candidate_count - len(eliminated_candidate_ids)
        if len(top_candidate_ids) == active_candidate_count:
            break

        if highest_vote_count > majority:
            break

        eliminated_candidate_ids.update(bottom_candidate_ids)

    return [
        candidate_name
        for candidate_id, candidate_name in enumerate(candidates)
        if candidate_id in top_candidate_ids
    ]


def main():
    candidate_count: int = int(input())
    candidates: list[str] = []

    for i in range(candidate_count):
        candidates.append(input())

    ballots: list[list[int]] = []

    while True:
        ballot = [int(i) for i in input().split(" ")]
        if not ballot:
            break
        ballots.append(ballot)

    print(solve_voting(candidates, ballots))


if __name__ == "__main__":
    main()

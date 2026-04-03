from engine import generate_candidates, score_party, get_party_rank


def print_candidates(role_name, candidates):
    print(f"\n{role_name} Candidates:")
    print("-" * 40)

    for i, candidate in enumerate(candidates, start=1):
        print(f"{i}. {candidate['race'].title()} {candidate['class']}")
        for stat, value in candidate["stats"].items():
            print(f"   {stat.title()}: {value}")
        print()


def choose_candidate(role_name, slot_name):
    candidates = generate_candidates(role_name, 3)
    print_candidates(slot_name, candidates)

    while True:
        choice = input(f"Choose your {slot_name} (1, 2, or 3): ").strip()

        if choice in ["1", "2", "3"]:
            selected = candidates[int(choice) - 1]
            selected["slot"] = slot_name
            print(f"\nYou selected: {selected['race'].title()} {selected['class']}\n")
            return selected

        print("Invalid choice. Please enter 1, 2, or 3.")


def print_final_party(party, total_party_score):
    party_rank = get_party_rank(total_party_score)
    print("\nFinal Party")
    print("=" * 50)

    for member in party:
        print(f"{member['slot']}: {member['race'].title()} {member['class']}")
        print(f"   Weighted Stat Score: {member['weighted_stat_score']}")
        print(f"   Duplicate Multiplier: {member['duplicate_multiplier']}")
        print(f"   Final Slot Score: {member['final_score']}")
        print()

    print("=" * 50)
    print(f"Total Party Score: {total_party_score}")
    print(f"Party Rank: {party_rank}")


def main():
    party = []

    party.append(choose_candidate("Leader", "Leader"))
    party.append(choose_candidate("Fighter", "Fighter 1"))
    party.append(choose_candidate("Fighter", "Fighter 2"))
    party.append(choose_candidate("Support", "Support 1"))
    party.append(choose_candidate("Support", "Support 2"))

    total_party_score = score_party(party)
    print_final_party(party, total_party_score)


if __name__ == "__main__":
    main()
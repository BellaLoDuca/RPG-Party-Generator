import random
from collections import Counter
from db import fetch_races, fetch_classes_for_role

stats = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]

ROLE_WEIGHTS = {
    "Leader": {
        "wisdom": 0.25,
        "intelligence": 0.25,
        "strength": 0.20,
        "charisma": 0.15,
        "constitution": 0.10,
        "dexterity": 0.05
    },
    "Fighter": {
        "strength": 0.25,
        "constitution": 0.25,
        "dexterity": 0.20,
        "wisdom": 0.15,
        "charisma": 0.10,
        "intelligence": 0.05
    },
    "Support": {
        "charisma": 0.25,
        "dexterity": 0.25,
        "intelligence": 0.20,
        "wisdom": 0.15,
        "constitution": 0.10,
        "strength": 0.05
    }
}

CLASS_REPEAT_PENALTY = 0.08
RACE_REPEAT_PENALTY = 0.05

PARTY_SLOTS = [
    ("Leader", "Leader"),
    ("Fighter", "Fighter 1"),
    ("Fighter", "Fighter 2"),
    ("Support", "Support 1"),
    ("Support", "Support 2")
]


def get_races():
    return fetch_races()


def generate_character(role_name):
    races = get_races()
    available_classes = fetch_classes_for_role(role_name)

    selected_class = random.choice(available_classes)
    selected_race = random.choice(races)

    final_stats = {}
    for stat in stats:
        final_stats[stat] = selected_class[stat] + selected_race[stat]

    return {
        "role": role_name,
        "class": selected_class["class_type"],
        "race": selected_race["race_type"],
        "suitability_score": float(selected_class["suitability_score"]),
        "stats": final_stats
    }


def generate_candidates(role_name, count=3):
    candidates = []
    used_combinations = set()

    while len(candidates) < count:
        character = generate_character(role_name)
        combo = (character["race"], character["class"])

        if combo not in used_combinations:
            used_combinations.add(combo)
            candidates.append(character)

    return candidates


def calculate_weighted_stat_score(character):
    role = character["role"]
    weights = ROLE_WEIGHTS[role]

    weighted_score = 0
    for stat, weight in weights.items():
        weighted_score += character["stats"][stat] * weight

    return weighted_score


def calculate_duplicate_multiplier(character, class_counts, race_counts):
    multiplier = 1.0

    class_repeats = class_counts[character["class"]] - 1
    race_repeats = race_counts[character["race"]] - 1

    if class_repeats > 0:
        multiplier *= (1 - (CLASS_REPEAT_PENALTY * class_repeats))

    if race_repeats > 0:
        multiplier *= (1 - (RACE_REPEAT_PENALTY * race_repeats))

    return max(multiplier, 0)


def score_party(party):
    class_counts = Counter(member["class"] for member in party)
    race_counts = Counter(member["race"] for member in party)

    total_party_score = 0

    for member in party:
        weighted_stat_score = calculate_weighted_stat_score(member)
        suitability_score = member["suitability_score"]
        duplicate_multiplier = calculate_duplicate_multiplier(member, class_counts, race_counts)

        final_score = weighted_stat_score * suitability_score * duplicate_multiplier

        member["weighted_stat_score"] = round(weighted_stat_score, 2)
        member["duplicate_multiplier"] = round(duplicate_multiplier, 3)
        member["final_score"] = round(final_score, 2)

        total_party_score += final_score

    return round(total_party_score, 2)


def get_party_rank(total_party_score):
    if total_party_score >= 55:
        return "S Tier"
    elif total_party_score >= 48:
        return "A Tier"
    elif total_party_score >= 40:
        return "B Tier"
    elif total_party_score >= 32:
        return "C Tier"
    else:
        return "D Tier"


def count_duplicate_instances(values):
    counts = Counter(values)
    return sum(count - 1 for count in counts.values() if count > 1)
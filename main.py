import numpy as np
import os
import string
import unicodedata

from itertools import product


def total_variation_distance(p, q):
    return 0.5 * sum(abs(p[c] - q[c]) for c in string.ascii_lowercase)


def collision_prob(p):
    return sum(p[c] ** 2 for c in string.ascii_lowercase)


def letter_frequencies(text, normalize=False):
    text = text.lower()

    '''
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    '''
    text = [c for c in text if c in string.ascii_lowercase]

    unique = set(text)

    assert unique == set(string.ascii_lowercase), unique

    counts = {c: text.count(c) for c in unique}

    if normalize:
        return {c: n / len(text) for c, n in counts.items()}
    else:
        return counts


if __name__ == "__main__":
    # Collect data.
    print(string.ascii_lowercase)
    corpii = {}

    for path in os.listdir("."):
        if "Alice" not in path:
            continue

        language = os.path.splitext(path)[0].split('_')[1]

        with open(path) as f:
            text = f.read()

        corpii[language] = letter_frequencies(text, True)

    with open("permuted_cipher.txt") as f:
        cipher = f.read()

    # Generate results for question a and b.
    distances = {}
    collisions = {}
    languages = sorted(corpii.keys())

    for idx, lang_p in enumerate(languages):
        p = corpii[lang_p]
        collisions[lang_p] = collision_prob(p)

        for lang_q in languages[idx:]:
            if lang_p == lang_q:
                continue

            q = corpii[lang_q]
            key = tuple(sorted([lang_p, lang_q]))
            distances[key] = total_variation_distance(p, q)

    closest = min(distances, key=distances.get)
    farthest = max(distances, key=distances.get)
    print(distances)
    print("Closest: {} <--> {} ({})".format(*closest, distances[closest]))
    print("Farthest: {} <--> {} ({})".format(*farthest, distances[farthest]))
    print(collisions)

    # Generate results for question d and e.
    p = letter_frequencies(cipher, True)

    distances = {
        lang: total_variation_distance(p, q)
        for lang, q in corpii.items()
    }

    distance_match = min(distances, key=distances.get)
    print(f"Minimal distance: {distance_match} ({distances[distance_match]})")

    cipher_coll = collision_prob(p)
    collision_diff = {
        lang: abs(coll - cipher_coll) for lang, coll in collisions.items()
    }
    collision_match = min(collision_diff, key=collision_diff.get)
    print(
        f"Minimal collision difference: {collision_match} "
        f"({collision_diff[collision_match]})"
    )

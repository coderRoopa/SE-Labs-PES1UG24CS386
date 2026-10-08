def evaluate(target, guess):
    """
    Return Wordle-style feedback for guess against target.

    Feedback values:
        green  = correct letter in the correct position
        yellow = correct letter in the wrong position
        gray   = letter does not have an available occurrence in target

    Exact matches are resolved first. Each occurrence in target can
    satisfy at most one occurrence in the guess.
    """

    if len(target) != len(guess):
        raise ValueError("Target and guess must have the same length.")

    result = ["gray"] * len(guess)

    # Count letters in target that have NOT already been used
    # by an exact match.
    remaining = {}

    # Pass 1: exact matches.
    for i, (target_ch, guess_ch) in enumerate(zip(target, guess)):
        if guess_ch == target_ch:
            result[i] = "green"
        else:
            remaining[target_ch] = remaining.get(target_ch, 0) + 1

    # Pass 2: present-but-wrong-position matches.
    for i, guess_ch in enumerate(guess):
        if result[i] == "green":
            continue

        if remaining.get(guess_ch, 0) > 0:
            result[i] = "yellow"
            remaining[guess_ch] -= 1

    return result
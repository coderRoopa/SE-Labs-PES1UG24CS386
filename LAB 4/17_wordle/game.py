import random

from words import WORDS
from feedback import evaluate


MAX_GUESSES = 6
SUPPORTED_LENGTHS = (4, 5, 6)


class WordleGame:
    def __init__(self, length=5, target=None):
        if length not in SUPPORTED_LENGTHS:
            raise ValueError(
                f"Unsupported word length: {length}. "
                f"Choose from {SUPPORTED_LENGTHS}."
            )

        self.length = length

        valid_words = [
            word.lower()
            for word in WORDS
            if len(word) == length and word.isalpha()
        ]

        if not valid_words:
            raise ValueError(
                f"No words of length {length} are available."
            )

        if target is not None:
            target = target.lower()

            if len(target) != length or not target.isalpha():
                raise ValueError(
                    "Target must be an alphabetic word of the selected length."
                )

            self.target = target
        else:
            self.target = random.choice(valid_words)

        # Only accepted guesses are stored here.
        self.history = []

        self.status = "playing"

    @property
    def guesses_used(self):
        return len(self.history)

    @property
    def guesses_remaining(self):
        return MAX_GUESSES - self.guesses_used

    def is_valid_guess(self, guess):
        """
        A valid guess must contain only alphabetic characters and
        have exactly the selected word length.
        """
        return (
            len(guess) == self.length
            and guess.isalpha()
        )

    def make_guess(self, guess):
        """
        Process one guess.

        Returns:
            feedback list for an accepted guess, or None for an invalid
            guess/guess made after the game has ended.
        """

        guess = guess.strip().lower()

        if self.status != "playing":
            return None

        # Invalid guesses do NOT consume a turn.
        if not self.is_valid_guess(guess):
            return None

        feedback = evaluate(self.target, guess)

        # Store only accepted guesses.
        self.history.append((guess, feedback))

        if guess == self.target:
            self.status = "won"
        elif self.guesses_used >= MAX_GUESSES:
            self.status = "lost"

        return feedback

    def quit(self):
        """End the game without adding a guess to history."""
        if self.status == "playing":
            self.status = "quit"

    def display_history(self):
        """Display all accepted guesses."""
        if not self.history:
            print("No accepted guesses yet.")
            return

        print("\nGuess history:")

        for number, (guess, feedback) in enumerate(self.history, start=1):
            formatted_feedback = " ".join(feedback)
            print(f"{number}. {guess:<{self.length}}  {formatted_feedback}")

    def display_summary(self):
        """Display the final game summary."""

        print("\nFinal summary")
        print("-" * 30)

        if self.status == "won":
            print(f"Solved in {self.guesses_used}/{MAX_GUESSES} guesses.")
        elif self.status == "lost":
            print(f"Out of guesses. The word was: {self.target}")
        elif self.status == "quit":
            print("Game quit.")
            print(f"The word was: {self.target}")

        print(f"Accepted guesses: {self.guesses_used}")
        print(f"Unused guesses: {self.guesses_remaining}")

        self.display_history()

    def run(self):
        print(
            f"Wordle — {self.length} letters, "
            f"{MAX_GUESSES} guesses."
        )

        while self.status == "playing":
            guess = input("> ").strip().lower()

            if guess == "q":
                self.quit()
                break

            if not self.is_valid_guess(guess):
                print(
                    f"Enter a valid {self.length}-letter word. "
                    "This attempt does not use a turn."
                )
                continue

            feedback = self.make_guess(guess)

            print(" ".join(feedback))

            # History is shown after every accepted guess.
            self.display_history()

            if self.status == "won":
                print("Solved!")
                break

            if self.status == "lost":
                print("No guesses remaining.")
                break

            print(f"Guesses remaining: {self.guesses_remaining}")

        self.display_summary()
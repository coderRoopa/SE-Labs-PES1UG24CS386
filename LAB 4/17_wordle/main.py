from game import WordleGame, SUPPORTED_LENGTHS


def choose_length():
    print("Choose a word length:")

    for length in SUPPORTED_LENGTHS:
        print(f"{length} - {length}-letter Wordle")

    while True:
        choice = input("> ").strip()

        if choice == "q":
            return None

        try:
            length = int(choice)
        except ValueError:
            print("Enter 4, 5, or 6.")
            continue

        if length in SUPPORTED_LENGTHS:
            return length

        print("Enter 4, 5, or 6.")


def main():
    length = choose_length()

    if length is None:
        print("Game quit.")
        return

    game = WordleGame(length=length)
    game.run()


if __name__ == "__main__":
    main()
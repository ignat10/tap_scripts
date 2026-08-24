from src.castles import add_castle, remove_castle


def main() -> None:
    command = input("Action (add/remove): ").strip().lower()
    name = input("Castle name: ").strip()
    match command:
        case "add":
            google = int(input("Google: "))
            add_castle(name, google)
            print(f"Added castle: {name}")
        case "remove":
            remove_castle(name)
            print(f"Removed castle: {name}")


if __name__ == "__main__":
    main()

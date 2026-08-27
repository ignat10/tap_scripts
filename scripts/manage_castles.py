import argparse
from pprint import pprint

from src.castles import (
    add_castle,
    get_castle,
    get_column,
    remove_all_castles,
    remove_castle,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage castles.")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="show all stored data when listing castles",
    )
    args = parser.parse_args()

    command = input("Action (add/remove/remove-all/list): ").strip().lower()
    match command:
        case "add":
            name = input("Castle name: ").strip()
            google = int(input("Google: "))
            add_castle(name, google)
            print(f"Added castle: {name}")
        case "remove":
            name = input("Castle name: ").strip()
            remove_castle(name)
            print(f"Removed castle: {name}")
        case "remove-all":
            confirmation = input("Delete ALL castles? Type DELETE to confirm: ").strip()
            if confirmation == "DELETE":
                deleted_count = remove_all_castles()
                print(f"Removed {deleted_count} castles")
            else:
                print("Cancelled")
        case "list":
            names = get_column("name")
            if args.verbose:
                for name in names:
                    pprint(get_castle(name), sort_dicts=False)
            else:
                pprint(names)


if __name__ == "__main__":
    main()

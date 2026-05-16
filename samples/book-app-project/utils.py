from datetime import datetime
from typing import Sequence

from books import Book


def prompt_non_empty(field_name: str) -> str:
    while True:
        value = input(f"Enter {field_name}: ").strip()
        if value:
            return value

        print(f"{field_name.capitalize()} cannot be empty.")


def parse_year(year_input: str) -> int:
    current_year = datetime.now().year
    cleaned_year = year_input.strip()

    if not cleaned_year:
        raise ValueError("Publication year cannot be empty.")

    try:
        year = int(cleaned_year)
    except ValueError as exc:
        raise ValueError("Publication year must be a whole number.") from exc

    if year < 0 or year > current_year:
        raise ValueError(f"Publication year must be between 0 and {current_year}.")

    return year


def print_menu() -> None:
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    while True:
        choice = input("Choose an option (1-5): ").strip()

        if not choice:
            print("Menu choice cannot be empty.")
            continue

        if not choice.isdigit():
            print("Menu choice must be a number.")
            continue

        return choice


def get_book_details() -> tuple[str, str, int]:
    title = prompt_non_empty("book title")
    author = prompt_non_empty("author")

    while True:
        year_input = input("Enter publication year: ").strip()
        try:
            year = parse_year(year_input)
            break
        except ValueError as error:
            print(error)

    return title, author, year


def print_books(books: Sequence[Book]) -> None:
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")

import os
import sys
from datetime import datetime

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from books import Book
from utils import get_book_details, get_user_choice, parse_year, print_books, prompt_non_empty


def test_parse_year_returns_integer_for_valid_input():
    assert parse_year("1949") == 1949


def test_parse_year_rejects_empty_input():
    with pytest.raises(ValueError, match="cannot be empty"):
        parse_year("   ")


def test_parse_year_rejects_non_numeric_input():
    with pytest.raises(ValueError, match="whole number"):
        parse_year("nineteen eighty four")


def test_parse_year_rejects_out_of_range_input():
    next_year = datetime.now().year + 1

    with pytest.raises(ValueError, match="must be between 0 and"):
        parse_year(str(next_year))


def test_prompt_non_empty_reprompts_until_value_is_provided(monkeypatch, capsys):
    responses = iter(["   ", "Dune"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    result = prompt_non_empty("book title")

    captured = capsys.readouterr()
    assert result == "Dune"
    assert "Book title cannot be empty." in captured.out


def test_get_book_details_reprompts_until_year_is_valid(monkeypatch, capsys):
    responses = iter(["Dune", "Frank Herbert", "abc", "1965"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    result = get_book_details()

    captured = capsys.readouterr()
    assert result == ("Dune", "Frank Herbert", 1965)
    assert "Publication year must be a whole number." in captured.out


def test_get_user_choice_reprompts_until_non_empty_value_is_provided(monkeypatch, capsys):
    responses = iter(["   ", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    result = get_user_choice()

    captured = capsys.readouterr()
    assert result == "2"
    assert "Menu choice cannot be empty." in captured.out


def test_get_user_choice_reprompts_until_numeric_value_is_provided(monkeypatch, capsys):
    responses = iter(["abc", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    result = get_user_choice()

    captured = capsys.readouterr()
    assert result == "4"
    assert "Menu choice must be a number." in captured.out


def test_print_books_displays_empty_collection_message(capsys):
    print_books([])

    captured = capsys.readouterr()
    assert "No books in your collection." in captured.out


def test_print_books_displays_books_with_read_status(capsys):
    books = [
        Book(title="Dune", author="Frank Herbert", year=1965, read=False),
        Book(title="Neuromancer", author="William Gibson", year=1984, read=True),
    ]

    print_books(books)

    captured = capsys.readouterr()
    assert "1. Dune by Frank Herbert (1965) - 📖 Unread" in captured.out
    assert "2. Neuromancer by William Gibson (1984) - ✅ Read" in captured.out

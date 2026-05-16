import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import book_app
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_collection(tmp_path, monkeypatch):
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
    book_app.collection = BookCollection()


def test_handle_read_marks_existing_book_as_read(monkeypatch, capsys):
    book_app.collection.add_book("Dune", "Frank Herbert", 1965)
    monkeypatch.setattr("builtins.input", lambda _: "Dune")

    book_app.handle_read()

    captured = capsys.readouterr()
    assert "Book marked as read." in captured.out
    assert book_app.collection.find_book_by_title("Dune").read is True


def test_handle_read_reports_missing_book(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "Missing Book")

    book_app.handle_read()

    captured = capsys.readouterr()
    assert "Book not found." in captured.out


def test_show_help_lists_read_command(capsys):
    book_app.show_help()

    captured = capsys.readouterr()
    assert "read     - Mark a book as read" in captured.out


def test_main_dispatches_read_command(monkeypatch):
    called = {"read": False}

    def fake_handle_read():
        called["read"] = True

    monkeypatch.setattr(book_app, "handle_read", fake_handle_read)
    monkeypatch.setattr(sys, "argv", ["book_app.py", "read"])

    book_app.main()

    assert called["read"] is True

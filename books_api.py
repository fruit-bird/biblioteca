""" 
Python client for the Google Books API

Write module documentation here
"""

import requests
from dataclasses import dataclass


class GoogleBooksAPI:
    API_URL = "https://www.googleapis.com/books/v1/volumes"

    @dataclass
    class Book:
        isbn: str
        title: str
        authors: list[str] | None
        description: str | None
        thumbnail_url: str | None
        # avg_rating: str
        # page_count: str
        # categories: list[str]

#         def __repr__(self) -> str:
#             return f"\
# ISBN13:\t\t\t{self.isbn}\n\
# Title:\t\t\t{self.title}\n\
# Author(s):\t\t{self.authors}\n\
# Description:\t\t{self.description}\n"

    @staticmethod
    def fetch_book(search_query: str):
        """
        Find the top matching book from the `search_query`

        >>> book = GoogleBooksAPI.fetch_book("Little Fires Everywhere")
        >>> if book is not None:
        >>>     print(book)

        ## Returns
        The first matching `Book`, or `None` if there is no match
        """
        params = {
            "q": search_query,
            "langRestrict": "en",
            "maxResults": 1,
            "printType": "books",
        }
        response = requests.get(GoogleBooksAPI.API_URL, params)

        if response.status_code == 200:
            data = response.json()
        else:
            return

        items = data.get("items", [])
        if items:
            first_book = items[0]["volumeInfo"]
            industry_identifiers = first_book.get("industryIdentifiers", [])
            isbn = (
                industry_identifiers[1]["identifier"]
                if len(industry_identifiers) > 1
                else industry_identifiers[0]["identifier"]
            )

            book = GoogleBooksAPI.Book(
                isbn,
                first_book["title"],
                first_book.get("authors"),
                first_book.get("description"),
                first_book["imageLinks"]["thumbnail"]
                if "imageLinks" in first_book
                else None,
            )
            return book

    @staticmethod
    # add kwargs so user can specify what other fields they want
    def fetch_n_books(search_query: str, n: int):
        """
        Returns a list of `n` `Book`s or `None`s

        >>> book = GoogleBooksAPI.fetch_n_books("Little Fires Everywhere")
        >>> if book is not None:
        >>>     print(book)
        """
        params = {
            "q": search_query,
            "langRestrict": "en",
            "maxResults": n,
            "printType": "books",
        }
        response = requests.get(GoogleBooksAPI.API_URL, params)

        if response.status_code == 200:
            data = response.json()
        else:
            return

        items = data.get("items", [])
        books = []

        for item in items[:n]:
            volume_info = item["volumeInfo"]
            industry_identifiers = volume_info.get("industryIdentifiers", [])
            isbn = (
                industry_identifiers[1]["identifier"]
                if len(industry_identifiers) > 1
                else industry_identifiers[0]["identifier"]
            )

            book = GoogleBooksAPI.Book(
                isbn,
                volume_info["title"],
                volume_info.get("authors"),
                volume_info.get("description"),
                volume_info["imageLinks"]["thumbnail"]
                if "imageLinks" in volume_info
                else None,
            )
            books.append(book)

        return books


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetches info about a book")
    parser.add_argument(
        "identifier",
        help="Anything that could help identify the book (title, ISBN, author name...)",
    )
    args = parser.parse_args()

    book = GoogleBooksAPI.fetch_book(args.identifier)
    # for book in books:
    print(book)

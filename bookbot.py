#!/usr/bin/env python3
"""BookBot - A simple CLI book recommendation bot."""

import random

BOOKS = [
    {
        "title": "The Name of the Wind",
        "author": "Patrick Rothfuss",
        "genres": ["fantasy", "adventure", "magic"],
        "description": "A legendary wizard recounts his extraordinary life.",
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "genres": ["sci-fi", "adventure", "political"],
        "description": "An epic tale of politics, religion, and survival on a desert planet.",
    },
    {
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "genres": ["sci-fi", "comedy", "adventure"],
        "description": "A hapless human is swept into an absurd journey across the universe.",
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "genres": ["dystopian", "political", "thriller"],
        "description": "A chilling portrait of a totalitarian society under constant surveillance.",
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "genres": ["romance", "classic", "drama"],
        "description": "A witty tale of love, class, and misunderstanding in Regency England.",
    },
    {
        "title": "The Girl with the Dragon Tattoo",
        "author": "Stieg Larsson",
        "genres": ["thriller", "mystery", "crime"],
        "description": "A journalist and hacker investigate a decades-old disappearance.",
    },
    {
        "title": "Sapiens",
        "author": "Yuval Noah Harari",
        "genres": ["non-fiction", "history", "science"],
        "description": "A sweeping history of humankind from the Stone Age to the present.",
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "genres": ["adventure", "philosophy", "fiction"],
        "description": "A shepherd boy's journey to find his personal legend.",
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "genres": ["classic", "drama", "historical"],
        "description": "A young girl witnesses racial injustice in the American South.",
    },
    {
        "title": "Neuromancer",
        "author": "William Gibson",
        "genres": ["sci-fi", "cyberpunk", "thriller"],
        "description": "A washed-up hacker is hired for one last job in cyberspace.",
    },
    {
        "title": "The Martian",
        "author": "Andy Weir",
        "genres": ["sci-fi", "adventure", "comedy"],
        "description": "An astronaut stranded on Mars must use science to survive.",
    },
    {
        "title": "Gone Girl",
        "author": "Gillian Flynn",
        "genres": ["thriller", "mystery", "crime"],
        "description": "A husband becomes the prime suspect when his wife vanishes.",
    },
    {
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "genres": ["non-fiction", "psychology", "science"],
        "description": "Explores the two systems that drive the way we think.",
    },
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "genres": ["fantasy", "adventure", "classic"],
        "description": "A reluctant hobbit sets off on an unexpected quest with a band of dwarves.",
    },
    {
        "title": "Flowers for Algernon",
        "author": "Daniel Keyes",
        "genres": ["sci-fi", "drama", "philosophy"],
        "description": "A man with an intellectual disability undergoes an experiment to increase his intelligence.",
    },
]

ALL_GENRES = sorted(
    set(genre for book in BOOKS for genre in book["genres"])
)


def print_header():
    print("\n" + "=" * 50)
    print("        Welcome to BookBot!")
    print("   Your personal book recommendation bot")
    print("=" * 50 + "\n")


def show_genres():
    print("Available genres:")
    for i, genre in enumerate(ALL_GENRES, 1):
        print(f"  {i:2}. {genre}")
    print()


def get_genre_choices():
    show_genres()
    raw = input("Enter genre numbers (comma-separated) or genre names: ").strip()
    if not raw:
        return []

    chosen = []
    parts = [p.strip() for p in raw.split(",")]

    for part in parts:
        if part.isdigit():
            idx = int(part) - 1
            if 0 <= idx < len(ALL_GENRES):
                chosen.append(ALL_GENRES[idx])
        elif part.lower() in ALL_GENRES:
            chosen.append(part.lower())
        else:
            # partial match
            matches = [g for g in ALL_GENRES if part.lower() in g]
            chosen.extend(matches)

    return list(set(chosen))


def recommend(genres, count=3):
    if not genres:
        return random.sample(BOOKS, min(count, len(BOOKS)))

    scored = []
    for book in BOOKS:
        score = sum(1 for g in genres if g in book["genres"])
        if score > 0:
            scored.append((score, book))

    scored.sort(key=lambda x: x[0], reverse=True)

    if not scored:
        print("No exact matches found. Here are some random picks:\n")
        return random.sample(BOOKS, min(count, len(BOOKS)))

    top_score = scored[0][0]
    top_books = [b for s, b in scored if s == top_score]

    if len(top_books) >= count:
        return random.sample(top_books, count)

    result = top_books[:]
    remaining = [b for s, b in scored if s < top_score]
    result += remaining[: count - len(result)]
    return result


def display_recommendations(books):
    print("\n" + "-" * 50)
    print(f"  Recommended books for you:")
    print("-" * 50)
    for i, book in enumerate(books, 1):
        print(f"\n  {i}. {book['title']}")
        print(f"     Author : {book['author']}")
        print(f"     Genres : {', '.join(book['genres'])}")
        print(f"     About  : {book['description']}")
    print("\n" + "-" * 50)


def main():
    print_header()

    while True:
        print("What would you like to do?")
        print("  1. Get book recommendations")
        print("  2. Browse all books")
        print("  3. Quit")
        choice = input("\nYour choice (1/2/3): ").strip()

        if choice == "1":
            print("\nTell me what genres you enjoy.")
            genres = get_genre_choices()
            if genres:
                print(f"\nLooking for books in: {', '.join(genres)}")
            else:
                print("\nNo genres selected. Showing random recommendations.")
            books = recommend(genres)
            display_recommendations(books)

        elif choice == "2":
            print("\n" + "-" * 50)
            print(f"  All {len(BOOKS)} books in the library:")
            print("-" * 50)
            for i, book in enumerate(BOOKS, 1):
                print(f"\n  {i:2}. {book['title']} — {book['author']}")
                print(f"       Genres: {', '.join(book['genres'])}")
            print("\n" + "-" * 50)

        elif choice == "3":
            print("\nHappy reading! Goodbye.\n")
            break

        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")

        print()


if __name__ == "__main__":
    main()

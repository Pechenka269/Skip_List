from data_loader import DataLoader


def main():
    loader = DataLoader()
    movies = loader.load_from_csv("horror_movies.csv")

    if movies:
        print("\nПримеры фильмов:")
        for i, movie in enumerate(list(movies.values())[:3]):
            print(f"{i + 1}. {movie['title']} - {movie['release_date']}")


if __name__ == "__main__":
    main()
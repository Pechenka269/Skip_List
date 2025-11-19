import csv
from datetime import datetime
from typing import Dict, Any


class DataLoader:
    def __init__(self):
        self.movies: Dict[int, Dict[str, Any]] = {}

    def load_from_csv(self, filename: str) -> Dict[int, Dict[str, Any]]:
        print("Загружаем данные о фильмах...")

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                movies_loaded = 0

                for row in reader:
                    try:
                        movie_id = int(row['id'])

                        release_date = None
                        if row['release_date']:
                            release_date = datetime.strptime(row['release_date'], '%Y-%m-%d')

                        vote_average = float(row['vote_average']) if row['vote_average'] else 0.0

                        self.movies[movie_id] = {
                            'id': movie_id,
                            'title': row['title'],
                            'release_date': release_date,
                            'vote_average': vote_average,
                            'overview': row['overview'],
                            'genre_names': row['genre_names']
                        }
                        movies_loaded += 1

                    except (ValueError, KeyError):
                        continue

                print(f"Успешно загружено {movies_loaded} фильмов")
                return self.movies

        except FileNotFoundError:
            print(f"Файл {filename} не найден")
            return {}
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
            return {}
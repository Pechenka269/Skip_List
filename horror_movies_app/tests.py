import unittest
from datetime import datetime
from data_loader import DataLoader
from search_index import SkipList, SearchIndex


class TestSkipList(unittest.TestCase):
    def test_insert_and_search(self):
        sl = SkipList()
        sl.insert(1, "test1")
        sl.insert(3, "test3")
        sl.insert(2, "test2")

        results = sl.search_range(1, 2)
        self.assertEqual(len(results), 2)
        self.assertIn("test1", results)
        self.assertIn("test2", results)


class TestSearchIndex(unittest.TestCase):
    def setUp(self):
        self.search_index = SearchIndex()
        self.test_movies = {
            1: {'id': 1, 'title': 'Test 1', 'release_date': datetime(2020, 1, 1), 'vote_average': 7.5, 'overview': '',
                'genre_names': ''},
            2: {'id': 2, 'title': 'Test 2', 'release_date': datetime(2021, 1, 1), 'vote_average': 8.0, 'overview': '',
                'genre_names': ''},
        }
        self.search_index.build_indexes(self.test_movies)

    def test_combined_search(self):
        results = self.search_index.search_combined(
            datetime(2020, 1, 1), datetime(2021, 12, 31),
            7.0, 8.5, self.test_movies
        )
        self.assertEqual(len(results), 2)


class TestDataLoader(unittest.TestCase):
    def test_load_data(self):
        loader = DataLoader()
        movies = loader.load_from_csv("horror_movies.csv")
        self.assertGreater(len(movies), 0)


if __name__ == "__main__":
    unittest.main()
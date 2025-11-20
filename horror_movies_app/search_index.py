import random
from typing import Any, List, Optional, Dict
from datetime import datetime


class SkipListNode:
    def __init__(self, key: Any, value: Any, level: int):
        self.key = key
        self.value = value
        self.forward = [None] * (level + 1)


class SkipList:
    def __init__(self, max_level: int = 16, p: float = 0.5):
        self.max_level = max_level
        self.p = p
        self.header = SkipListNode(None, None, max_level)
        self.level = 0

    def _random_level(self) -> int:
        level = 0
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level

    def insert(self, key: Any, value: Any):
        update = [None] * (self.max_level + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        new_level = self._random_level()
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level

        new_node = SkipListNode(key, value, new_level)
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def search_range(self, start_key: Any, end_key: Any) -> List[Any]:
        results = []
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < start_key:
                current = current.forward[i]

        current = current.forward[0]
        while current and current.key <= end_key:
            results.append(current.value)
            current = current.forward[0]

        return results


class SearchIndex:
    def __init__(self):
        self.release_date_index = SkipList()
        self.vote_average_index = SkipList()

    def build_indexes(self, movies: Dict[int, Dict[str, Any]]):

        for movie_id, movie in movies.items():
            if movie['release_date']:
                self.release_date_index.insert(movie['release_date'], movie_id)
            self.vote_average_index.insert(movie['vote_average'], movie_id)

    def search_combined(self, start_date: Optional[datetime], end_date: Optional[datetime],
                        min_rating: Optional[float], max_rating: Optional[float],
                        movies: Dict[int, Dict[str, Any]]) -> List[Dict[str, Any]]:
        date_ids = set()
        rating_ids = set()

        if start_date and end_date:
            date_ids = set(self.release_date_index.search_range(start_date, end_date))

        if min_rating is not None and max_rating is not None:
            rating_ids = set(self.vote_average_index.search_range(min_rating, max_rating))

        if date_ids and rating_ids:
            final_ids = date_ids.intersection(rating_ids)
        elif date_ids:
            final_ids = date_ids
        elif rating_ids:
            final_ids = rating_ids
        else:
            return []

        return [movies[movie_id] for movie_id in final_ids]
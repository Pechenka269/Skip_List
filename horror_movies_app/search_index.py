import random
from typing import Any, List, Dict


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
        self.date_index = SkipList()
        self.rating_index = SkipList()
    def build_indexes(self, movies: Dict[int, Dict[str, Any]]):

        for movie_id, movie in movies.items():
            if movie['release_date']:
                self.date_index.insert(movie['release_date'], movie_id)
            self.rating_index.insert(movie['vote_average'], movie_id)


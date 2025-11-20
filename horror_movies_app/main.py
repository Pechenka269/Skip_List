import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from data_loader import DataLoader
from search_index import SearchIndex


class HorrorMoviesApp:
    def __init__(self):
        self.root = tk.Tk()
        self.data_loader = DataLoader()
        self.search_index = SearchIndex()
        self.movies = {}

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        self.root.title("Поиск фильмов ужасов")
        self.root.geometry("900x700")

        # Фрейм поиска
        search_frame = ttk.LabelFrame(self.root, text="Параметры поиска", padding=10)
        search_frame.pack(padx=10, pady=5, fill="x")

        # Поиск по дате
        date_frame = ttk.Frame(search_frame)
        date_frame.pack(fill="x", pady=5)

        ttk.Label(date_frame, text="Дата релиза от:").grid(row=0, column=0, sticky="w")
        self.start_date_entry = ttk.Entry(date_frame, width=12)
        self.start_date_entry.grid(row=0, column=1, padx=5)
        ttk.Label(date_frame, text="ГГГГ-ММ-ДД").grid(row=0, column=2)

        ttk.Label(date_frame, text="до:").grid(row=0, column=3)
        self.end_date_entry = ttk.Entry(date_frame, width=12)
        self.end_date_entry.grid(row=0, column=4, padx=5)
        ttk.Label(date_frame, text="ГГГГ-ММ-ДД").grid(row=0, column=5)

        # Поиск по рейтингу
        rating_frame = ttk.Frame(search_frame)
        rating_frame.pack(fill="x", pady=5)

        ttk.Label(rating_frame, text="Рейтинг от:").grid(row=0, column=0, sticky="w")
        self.min_rating_entry = ttk.Entry(rating_frame, width=8)
        self.min_rating_entry.grid(row=0, column=1, padx=5)

        ttk.Label(rating_frame, text="до:").grid(row=0, column=2)
        self.max_rating_entry = ttk.Entry(rating_frame, width=8)
        self.max_rating_entry.grid(row=0, column=3, padx=5)

        # Кнопки
        button_frame = ttk.Frame(search_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Поиск по дате",
                   command=self.search_by_date).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Поиск по рейтингу",
                   command=self.search_by_rating).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Комбинированный поиск",
                   command=self.search_combined).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Сбросить",
                   command=self.clear_search).pack(side="left", padx=5)
        self.stats_label = ttk.Label(search_frame, text="Загружено фильмов: 0")
        self.stats_label.pack()

        results_frame = ttk.LabelFrame(self.root, text="Результаты поиска", padding=10)
        results_frame.pack(padx=10, pady=5, fill="both", expand=True)

        columns = ("Название", "Дата релиза", "Рейтинг", "Жанры")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=12)

        column_widths = [250, 120, 80, 200]
        for col, width in zip(columns, column_widths):
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=width)

        tree_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=tree_scrollbar.set)

        self.results_tree.pack(side="left", fill="both", expand=True)
        tree_scrollbar.pack(side="right", fill="y")

        details_frame = ttk.LabelFrame(self.root, text="Детальная информация", padding=10)
        details_frame.pack(padx=10, pady=5, fill="x")

        self.details_text = tk.Text(details_frame, height=6, wrap="word")
        details_scrollbar = ttk.Scrollbar(details_frame, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scrollbar.set)

        self.details_text.pack(side="left", fill="both", expand=True)
        details_scrollbar.pack(side="right", fill="y")

        self.results_tree.bind("<<TreeviewSelect>>", self.on_movie_select)

    def load_data(self):
        self.movies = self.data_loader.load_from_csv("horror_movies.csv")
        if self.movies:
            self.search_index.build_indexes(self.movies)
            self.stats_label.config(text=f"Загружено фильмов: {len(self.movies)}")

    def search_by_date(self):
        try:
            start_date = self.parse_date(self.start_date_entry.get())
            end_date = self.parse_date(self.end_date_entry.get())

            movie_ids = self.search_index.release_date_index.search_range(start_date, end_date)
            results = [self.movies[movie_id] for movie_id in movie_ids]
            self.display_results(results, f"Найдено фильмов по дате: {len(results)}")

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def search_by_rating(self):
        try:
            min_rating = self.parse_rating(self.min_rating_entry.get())
            max_rating = self.parse_rating(self.max_rating_entry.get())

            if min_rating > max_rating:
                messagebox.showerror("Ошибка", "Минимальный рейтинг не может быть больше максимального!")
                return

            movie_ids = self.search_index.vote_average_index.search_range(min_rating, max_rating)
            results = [self.movies[movie_id] for movie_id in movie_ids]
            self.display_results(results, f"Найдено фильмов по рейтингу: {len(results)}")

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def search_combined(self):
        try:
            start_date = None
            end_date = None
            min_rating = None
            max_rating = None

            if self.start_date_entry.get():
                start_date = self.parse_date(self.start_date_entry.get())
                end_date = self.parse_date(self.end_date_entry.get())

            if self.min_rating_entry.get():
                min_rating = self.parse_rating(self.min_rating_entry.get())
                max_rating = self.parse_rating(self.max_rating_entry.get())
                if min_rating > max_rating:
                    messagebox.showerror("Ошибка", "Минимальный рейтинг не может быть больше максимального!")
                    return

            results = self.search_index.search_combined(
                start_date, end_date, min_rating, max_rating, self.movies
            )
            self.display_results(results, f"Найдено фильмов: {len(results)}")

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def parse_date(self, date_str: str) -> datetime:
        if not date_str:
            raise ValueError("Дата не может быть пустой!")
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Неверный формат даты! Используйте ГГГГ-ММ-ДД")

    def parse_rating(self, rating_str: str) -> float:
        if not rating_str:
            raise ValueError("Рейтинг не может быть пустым!")
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                raise ValueError("Рейтинг должен быть от 0 до 10")
            return rating
        except ValueError:
            raise ValueError("Рейтинг должен быть числом!")

    def display_results(self, results: list, status: str = ""):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        for movie in results:
            release_date = movie['release_date'].strftime("%Y-%m-%d") if movie['release_date'] else "N/A"
            self.results_tree.insert("", "end", values=(
                movie['title'],
                release_date,
                f"{movie['vote_average']:.1f}",
                movie['genre_names']
            ))

        if status:
            self.stats_label.config(text=status)

    def clear_search(self):
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.min_rating_entry.delete(0, tk.END)
        self.max_rating_entry.delete(0, tk.END)

        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        self.details_text.delete(1.0, tk.END)
        self.stats_label.config(text=f"Загружено фильмов: {len(self.movies)}")

    def on_movie_select(self, event):
        selection = self.results_tree.selection()
        if not selection:
            return

        item = selection[0]
        movie_title = self.results_tree.item(item)['values'][0]

        movie = None
        for m in self.movies.values():
            if m['title'] == movie_title:
                movie = m
                break

        if movie:
            self.display_movie_details(movie)

    def display_movie_details(self, movie: dict):
        self.details_text.delete(1.0, tk.END)

        details = f"{movie['title']}\n"
        details += f"Дата релиза: {movie['release_date'].strftime('%Y-%m-%d') if movie['release_date'] else 'N/A'}\n"
        details += f"Рейтинг: {movie['vote_average']:.1f}/10\n"
        details += f"Жанры: {movie['genre_names']}\n"

        if movie['overview']:
            details += f"\nОписание:\n{movie['overview']}\n"

        self.details_text.insert(1.0, details)

    def run(self):
        self.root.mainloop()


def main():
    app = HorrorMoviesApp()
    app.run()


if __name__ == "__main__":
    main()
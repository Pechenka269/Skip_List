import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from data_loader import DataLoader
from search_index import SearchIndex


class HorrorMoviesApp:
    def __init__(self):
        self.root = tk.Tk()
        self.loader = DataLoader()
        self.index = SearchIndex()
        self.movies = {}

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        self.root.title("Поиск фильмов ужасов")
        self.root.geometry("800x600")

        # Поиск
        search_frame = ttk.LabelFrame(self.root, text="Поиск", padding=10)
        search_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(search_frame, text="Дата от:").grid(row=0, column=0)
        self.start_date = ttk.Entry(search_frame, width=12)
        self.start_date.grid(row=0, column=1, padx=2)

        ttk.Label(search_frame, text="до:").grid(row=0, column=2)
        self.end_date = ttk.Entry(search_frame, width=12)
        self.end_date.grid(row=0, column=3, padx=2)

        ttk.Label(search_frame, text="Рейтинг от:").grid(row=1, column=0, pady=5)
        self.min_rating = ttk.Entry(search_frame, width=8)
        self.min_rating.grid(row=1, column=1, padx=2, pady=5)

        ttk.Label(search_frame, text="до:").grid(row=1, column=2, pady=5)
        self.max_rating = ttk.Entry(search_frame, width=8)
        self.max_rating.grid(row=1, column=3, padx=2, pady=5)

        ttk.Button(search_frame, text="Поиск по дате",
                   command=self.search_date).grid(row=0, column=4, padx=5)
        ttk.Button(search_frame, text="Поиск по рейтингу",
                   command=self.search_rating).grid(row=1, column=4, padx=5)

        # Результаты
        results_frame = ttk.LabelFrame(self.root, text="Результаты", padding=10)
        results_frame.pack(padx=10, pady=5, fill="both", expand=True)

        columns = ("Название", "Дата", "Рейтинг")
        self.tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_data(self):
        self.movies = self.loader.load_from_csv("horror_movies.csv")
        if self.movies:
            self.index.build_indexes(self.movies)

    def search_date(self):
        try:
            start = datetime.strptime(self.start_date.get(), "%Y-%m-%d")
            end = datetime.strptime(self.end_date.get(), "%Y-%m-%d")

            movie_ids = self.index.date_index.search_range(start, end)
            self.show_results([self.movies[mid] for mid in movie_ids])

        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты!")

    def search_rating(self):
        try:
            min_r = float(self.min_rating.get())
            max_r = float(self.max_rating.get())

            movie_ids = self.index.rating_index.search_range(min_r, max_r)
            self.show_results([self.movies[mid] for mid in movie_ids])

        except ValueError:
            messagebox.showerror("Ошибка", "Введите числа для рейтинга!")

    def show_results(self, results):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for movie in results:
            date_str = movie['release_date'].strftime("%Y-%m-%d") if movie['release_date'] else "N/A"
            self.tree.insert("", "end", values=(
                movie['title'], date_str, f"{movie['vote_average']:.1f}"
            ))


def main():
    app = HorrorMoviesApp()
    app.root.mainloop()


if __name__ == "__main__":
    main()
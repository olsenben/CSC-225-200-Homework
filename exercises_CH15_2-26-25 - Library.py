
class Creator:
    def __init__(self, name, year_of_birth):
        self.name = name
        self.year_of_birth = year_of_birth

    def __str__(self):
        return f"{self.name} (born {self.birth_year})"


class MediaItem:
    def __init__(self, title, year, genre):
        self.title = title
        self.year = year
        self.genre = genre

class Book(MediaItem):
    def __init__(self, title, year, genre, author_name, author_birth_year, num_pages):
        super().__init__(title, year, genre)
        self.author = Creator(author_name, author_birth_year)
        self.num_pages = num_pages

    def __str__(self):
        return f"{self.title}, by {self.author}"

class Dvd(MediaItem):
    def __init__(self, title, year, genre, director_name, director_birth_year, actor):
        super().__init__(title, year, genre)
        self.director = Creator(director_name, director_birth_year)
        self.actor = actor

    def __str__(self):
        return f"{self.title}, directed by {self.director}"

jasmines_book = Book("the poppy war", 2028, "fantasy", "RF Kuang",1990, 300)
jasmines_dvd = Dvd("Inglorious Bastards", 2010, "action", "tarintino", "Brad Pitt")

print(jasmines_book)
print(jasmines_dvd)

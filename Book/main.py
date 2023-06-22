import random


class Book:
    def __init__(self, name, genre, release_year, author, rating):
        self.name = name
        self.genre = genre
        self.release_year = release_year
        self.author = author
        self._rating = rating
        self.__ISBN = random.randint(100000000000000, 999999999999999)

    def read(self):
        return f"Someone is reading {self.name} of genre: {self.genre}. "


class ComedyBook(Book):
    def __int__(self, name, genre, release_year, author, rating, comedy_genre):
        self.comedy_genre = comedy_genre
        super().__init__(name, genre, release_year, author, rating)

    def __str__(self):
        return f"Name: {self.name}\nGenre: {self.genre}\nRelease Year: {self.release_year}\n" \
               f"Author: {self.author}\nRating: {self._rating}\n"

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating_set(self, rating: float):
        if 0 <= rating <= 10:
            self._rating = rating
        else:
            print("Invalid Rating Number")


book1 = ComedyBook('Davit', 'Comedy', '2020', 'Mamuli', '5.5')
print(book1)

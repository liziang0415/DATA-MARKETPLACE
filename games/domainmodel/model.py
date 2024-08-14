from datetime import datetime


class Tag:
    def __init__(self, tag_name: str):
        if tag_name == "" or type(tag_name) is not str:
            self.__tag_name = None
        else:
            self.__tag_name = tag_name.strip()

    @property
    def tag_name(self) -> str:
        return self.__tag_name

    def __repr__(self) -> str:
        return f'<Genre {self.__tag_name}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.tag_name == self.__tag_name

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__tag_name < other.tag_name

    def __hash__(self):
        return hash(self.__tag_name)


class Thread:
    def __init__(self, thread_id: int, thread_title: str, thread_content: str):
        if type(thread_id) is not int or thread_id < 0:
            raise ValueError("Game ID should be a positive integer!")
        self.__thread_id = thread_id

        if type(thread_title) is str and thread_title.strip() != "":
            self.__thread_title = thread_title.strip()
        else:
            self.__thread_title = None

        self.__release_date = None
        self.__description = thread_content
        self.__tags: list = []
        self.__reviews: list = []

    @property
    def thread_id(self):
        return self.__thread_id

    @property
    def title(self):
        return self.__thread_title

    @title.setter
    def title(self, new_title):
        if type(new_title) is str and new_title.strip() != "":
            self.__thread_title = new_title.strip()
        else:
            self.__thread_title = None

    @property
    def release_date(self):
        return self.__release_date

    @release_date.setter
    def release_date(self, release_date: str):
        if isinstance(release_date, str):
            try:
                datetime.strptime(release_date, "%b %d, %Y")
                self.__release_date = release_date
            except ValueError:
                raise ValueError("Release date must be in 'Oct 21, 2008' format!")
        else:
            raise ValueError("Release date must be a string in 'Oct 21, 2008' format!")

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description: str):
        if isinstance(description, str) and description.strip() != "":
            self.__description = description
        else:
            self.__description = None

    @property
    def reviews(self) -> list:
        return self.__reviews

    @property
    def tags(self) -> list:
        return self.__tags

    def add_tag(self, tags: Tag):
        if not isinstance(tags, Tag) or tags in self.__tags:
            return
        self.__tags.append(tags)

    def remove_tag(self, tags: Tag):
        if not isinstance(tags, Tag):
            return
        try:
            self.__tags.remove(tags)
        except ValueError:
            print(f"Could not find {tags} in list of genres.")
            pass

    def average_rating(self):
        if len(self.__reviews) == 0:
            return "No ratings yet"
        total_rating = sum([review.rating for review in self.__reviews])
        return round(total_rating / len(self.__reviews), 2)

    def add_review(self, review):
        self.__reviews.append(review)

    def __repr__(self):
        return f"<Game {self.__thread_id}, {self.__thread_title}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__thread_id == other.__thread_id

    def __hash__(self):
        return hash(self.__thread_id)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__thread_id < other.thread_id


class User:
    def __init__(self, username: str, password: str, email: str, dob: str, gender: str):
        if not isinstance(username, str) or username.strip() == "":
            raise ValueError('Username cannot be empty or non-string!')
        else:
            self.__username = username.lower().strip()

        if isinstance(password, str) and len(password) >= 7:
            self.__password = password
        else:
            raise ValueError('Password not valid!')

        self.__reviews: list[Review] = []
        self.__favorite = None
        self.__email = email
        self.__dob = dob
        self.__gender = gender

    @property
    def username(self):
        return self.__username

    @property
    def password(self) -> str:
        return self.__password

    @property
    def reviews(self) -> list:
        return self.__reviews

    @property
    def dob(self) -> str:
        return self.__dob

    @property
    def email(self) -> str:
        return self.__email

    @property
    def gender(self):
        return self.__gender

    def add_review(self, new_review):
        if not isinstance(new_review, Review) or new_review in self.__reviews:
            return
        self.__reviews.append(new_review)

    def remove_review(self, review):
        if not isinstance(review, Review) or review not in self.__reviews:
            return
        self.__reviews.remove(review)

    @property
    def favorites(self):
        return self.__favorite

    @favorites.setter
    def favorites(self, favobj):
        if isinstance(favobj, Favorite):
            self.__favorite = favobj

    def __repr__(self):
        return f"<User {self.__username}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__username == other.username

    def __hash__(self):
        return hash(self.__username)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__username < other.username


class Review:
    def __init__(self, user: User, thread: Thread, rating: int, comment: str):

        if not isinstance(user, User):
            raise ValueError("User must be an instance of User class")
        self.__user = user

        if not isinstance(thread, Thread):
            raise ValueError("Game must be an instance of Game class")
        self.__thread = thread

        if not isinstance(rating, int) or not 0 <= rating <= 5:
            raise ValueError("Rating must be an integer between 0 and 5")
        self.__rating = rating

        if not isinstance(comment, str):
            raise ValueError("Comment must be a string")
        self.__comment = comment.strip()

    @property
    def game(self) -> Thread:
        return self.__thread

    @property
    def comment(self) -> str:
        return self.__comment

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def user(self) -> User:
        return self.__user

    @comment.setter
    def comment(self, new_text):
        if isinstance(new_text, str):
            self.__comment = new_text.strip()
        else:
            raise ValueError("New comment must be a string")

    @rating.setter
    def rating(self, new_rating: int):
        if isinstance(new_rating, int) and 0 <= new_rating <= 5:
            self.__rating = new_rating
        else:
            raise ValueError("Rating must be an integer between 0 and 5")

    def __repr__(self):
        return f"Review(User: {self.__user}, Game: {self.__thread}, " \
               f"Rating: {self.__rating}, Comment: {self.__comment})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.user == self.__user and other.__thread == self.__thread and other.comment == self.__comment


class Favorite:
    def __init__(self, user: User):
        if not isinstance(user, User):
            raise ValueError("User must be an instance of User class")
        self.__user = user

        self.__list_of_thread = []

    def list_of_thread(self):
        return self.__list_of_thread

    def size(self):
        size_wishlist = len(self.__list_of_thread)
        if size_wishlist > 0:
            return size_wishlist

    def add_thread(self, thread: Thread):
        if isinstance(thread, Thread) and thread not in self.__list_of_thread:
            self.__list_of_thread.append(thread)

    def first_game_in_list(self):
        if len(self.__list_of_thread) > 0:
            return self.__list_of_thread[0]
        else:
            return None

    def remove_thread(self, thread: Thread):
        if isinstance(thread, Thread) and thread in self.__list_of_thread:
            self.__list_of_thread.remove(thread)

    def select_game(self, index):
        if 0 <= index < len(self.__list_of_thread):
            return self.__list_of_thread[index]
        else:
            return None

    def __iter__(self):
        self.__current = 0
        return self

    def __next__(self):
        if self.__current >= len(self.__list_of_thread):
            raise StopIteration
        else:
            self.__current += 1
            return self.__list_of_thread[self.__current - 1]

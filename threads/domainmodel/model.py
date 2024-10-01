from datetime import datetime
from typing import List, Optional


class Tag:
    def __init__(self, tag_name: str):
        if tag_name == "" or type(tag_name) is not str:
            raise ValueError("Invalid tag name!")
        self.tag_name = tag_name.strip()

    def __repr__(self) -> str:
        return f'<Tag {self.tag_name}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.tag_name == self.tag_name

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.tag_name < other.tag_name

    def __hash__(self):
        return hash(self.tag_name)


class Thread:
    def __init__(self, thread_title: str, thread_content: str):
        self.id = None
        self.thread_title = thread_title
        self.release_date = None
        self.description = thread_content
        self.sold = False
        self.user: Optional['User'] = None
        self.tags: List['Tag'] = []
        self.reviews: List['Review'] = []
        self.purchasers: List['User'] = []

    def add_tag(self, tag: Tag):
        if isinstance(tag, Tag) and tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: Tag):
        if isinstance(tag, Tag) and tag in self.tags:
            self.tags.remove(tag)

    def average_rating(self):
        if len(self.reviews) == 0:
            return "No ratings yet"
        total_rating = sum([review.rating for review in self.reviews])
        return round(total_rating / len(self.reviews), 2)

    def add_review(self, review):
        self.reviews.append(review)

    def gettitle(self):
        return  self.thread_title

    def __repr__(self):
        return f"<Thread {self.thread_title}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.thread_title == other.thread_title

    def __hash__(self):
        return hash(self.thread_title)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.thread_title < other.thread_title


from typing import List, Optional


class User:
    def __init__(self, username: str, password: str, email: Optional[str] = None,
                 dob: Optional[str] = None, gender: Optional[str] = None, is_company: bool = False):
        print(
            f"Initializing User with: username={username}, password={password}, email={email}, dob={dob}, gender={gender}, is_company={is_company}")

        if not isinstance(username, str) or username.strip() == "":
            raise ValueError('Username cannot be empty or non-string!')
        self.username = username.lower().strip()

        if isinstance(password, str) and len(password) >= 7:
            self.password = password
        else:
            raise ValueError('Password must be at least 7 characters long!')

        self.email = email
        self.dob = dob
        self.gender = gender
        self.is_company = is_company
        self.reviews: List['Review'] = []
        self.threads: List['Thread'] = []
        self.purchased_threads: List['Thread'] = []
        self.favorite: Optional['Favorite'] = None

    def purchase_thread(self, thread: Thread):
        if isinstance(thread, Thread) and thread not in self.purchased_threads:
            self.purchased_threads.append(thread)
            thread.purchasers.append(self)
            thread.sold = True

    def add_review(self, new_review):
        if isinstance(new_review, Review) and new_review not in self.reviews:
            self.reviews.append(new_review)

    def remove_review(self, review):
        if review in self.reviews:
            self.reviews.remove(review)

    def add_thread(self, thread: Thread):
        if isinstance(thread, Thread) and thread not in self.threads:
            self.threads.append(thread)
            thread.user = self  # Set the user as the creator of the thread

    def remove_thread(self, thread: Thread):
        if thread in self.threads:
            self.threads.remove(thread)
            thread.user = None  # Remove the association with the user

    def get_fav(self):
        return self.favorite

    def __repr__(self):
        return f"<User {self.username}, {self.email}, Company: {self.is_company}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.username == other.username

    def __hash__(self):
        return hash(self.username)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.username < other.username


class Review:
    def __init__(self, user: User, thread: Thread, comment: str):

        if not isinstance(user, User):
            raise ValueError("User must be an instance of User class")
        self.user = user

        if not isinstance(thread, Thread):
            raise ValueError("Thread must be an instance of Thread class")
        self.thread = thread

        if not isinstance(comment, str):
            raise ValueError("Comment must be a string")
        self.comment = comment.strip()

    def __repr__(self):
        return f"Review(User: {self.user}, Thread: {self.thread}, " \
               f"Comment: {self.comment})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.user == self.user and other.thread == self.thread and other.comment == self.comment


class Favorite:
    def __init__(self, user: User):
        if not isinstance(user, User):
            raise ValueError("User must be an instance of User class")
        self.user = user
        self.list_of_threads = []

    def size(self):
        return len(self.list_of_threads)

    def add_thread(self, thread: Thread):
        if isinstance(thread, Thread) and thread not in self.list_of_threads:
            self.list_of_threads.append(thread)

    def first_thread_in_list(self):
        if len(self.list_of_threads) > 0:
            return self.list_of_threads[0]
        else:
            return None

    def remove_thread(self, thread: Thread):
        if isinstance(thread, Thread) and thread in self.list_of_threads:
            self.list_of_threads.remove(thread)

    def select_thread(self, index):
        if 0 <= index < len(self.list_of_threads):
            return self.list_of_threads[index]
        else:
            return None

    def __iter__(self):
        self.current = 0
        return self

    def __next__(self):
        if self.current >= len(self.list_of_threads):
            raise StopIteration
        else:
            self.current += 1
            return self.list_of_threads[self.current - 1]

import abc
from typing import List
from games.domainmodel.model import Thread,Tag, Favorite

repo_instance = None


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_thread(self, thread: Thread):
        raise NotImplementedError

    @abc.abstractmethod
    def get_threads(self) -> List[Thread]:
        raise NotImplementedError


    @abc.abstractmethod
    def add_tag(self, tag: Tag):
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_threads(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_for_thread(self, thread_title):
        raise NotImplementedError

    @abc.abstractmethod
    def add_to_fav(self, username, fav:Favorite):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_from_fav(self, username, fav:Favorite):
        raise NotImplementedError

    @abc.abstractmethod
    def get_fav(self, username):
        raise NotImplementedError

    @abc.abstractmethod
    def is_in_fav(self, username, thread_title):
        raise NotImplementedError

    @abc.abstractmethod
    def get_tag(self, tag_name):
        raise NotImplementedError

    @abc.abstractmethod
    def find_thread_by_title(self, title: str):
        raise NotImplementedError

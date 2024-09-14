import abc
from typing import List
from threads.domainmodel.model import Thread, Tag, Favorite, User, Review

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
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_for_thread(self, thread_title: str) -> List[Review]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_to_favorite(self, username: str, thread: Thread):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_from_favorite(self, username: str, thread: Thread):
        raise NotImplementedError

    @abc.abstractmethod
    def get_favorite(self, username: str) -> List[Thread]:
        raise NotImplementedError

    @abc.abstractmethod
    def is_in_favorite(self, username: str, thread: Thread) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get_tag(self, tag_name: str) -> Tag:
        raise NotImplementedError

    @abc.abstractmethod
    def find_thread_by_id(self, thread_id: int) -> Thread:
        raise NotImplementedError

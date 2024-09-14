from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import scoped_session

from threads.services import NameNotUniqueException
from .repository import AbstractRepository
from ..domainmodel import User, Tag, Thread, Favorite, Review


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_thread(self, thread: Thread):
        with self._session_cm as scm:
            scm.session.merge(thread)
            scm.commit()

    def get_threads(self) -> list[Thread]:
        return self._session_cm.session.query(Thread).all()

    def get_number_of_threads(self):
        return self._session_cm.session.query(Thread).count()

    def add_user(self, user: User):
        with self._session_cm as scm:
            print(f"Adding User: {user.username}, {user.password}, {user.email}, {user.dob}, {user.gender}")
            existing_user = scm.session.query(User).filter_by(username=user.username).first()
            if existing_user:
                raise NameNotUniqueException(f"Username {user.username} already exists!")
            scm.session.add(user)
            scm.commit()

    def get_user(self, username: str) -> User:
        return self._session_cm.session.query(User).filter_by(username=username.lower()).one_or_none()

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews_for_thread(self, thread_title: str) -> list[Review]:
        thread = self.find_thread_by_title(thread_title)
        return thread.reviews if thread else []

    def add_to_favorite(self, username: str, thread: Thread):
        with self._session_cm as scm:
            user = self.get_user(username)
            if user:
                favorite = user.favorite
                if not favorite:
                    favorite = Favorite(user)
                    user.favorite = favorite
                    scm.session.add(favorite)
                favorite.add_thread(thread)
                scm.commit()

    def remove_from_favorite(self, username: str, thread: Thread):
        with self._session_cm as scm:
            user = self.get_user(username)
            if user:
                favorite = user.favorite
                if favorite:
                    favorite.remove_thread(thread)
                    scm.commit()

    def get_favorite(self, username: str) -> list[Thread]:
        user = self.get_user(username)
        return user.favorite.list_of_thread() if user and user.favorite else []

    def is_in_favorite(self, username: str, thread: Thread) -> bool:
        user = self.get_user(username)
        return thread in user.favorite.list_of_threads() if user and user.favorite else False

    def get_tag(self, tag_name: str) -> Tag:
        return self._session_cm.session.query(Tag).filter_by(tag_name=tag_name.lower()).one_or_none()

    from sqlalchemy import func

    def add_tag(self, tag: Tag):
        with self._session_cm as scm:
            scm.session.merge(tag)
            scm.commit()

    def find_thread_by_id(self, thread_id: int) -> Thread:
        return self._session_cm.session.query(Thread).filter_by(id=thread_id).one_or_none()

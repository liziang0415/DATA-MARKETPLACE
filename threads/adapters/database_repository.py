from collections import defaultdict

from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import scoped_session

from threads.services import NameNotUniqueException
from .orm import thread_tags
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

    def get_reviews_for_thread(self, thread_id) -> list[Review]:
        thread = self.find_thread_by_id(thread_id)
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
        return thread in user.favorite.list_of_threads if user and user.favorite else False

    def get_tag(self, tag_name: str) -> Tag:
        return self._session_cm.session.query(Tag).filter_by(tag_name=tag_name.lower()).one_or_none()

    from sqlalchemy import func

    def add_tag(self, tag: Tag):
        with self._session_cm as scm:
            scm.session.merge(tag)
            scm.commit()

    def find_thread_by_id(self, thread_id: int) -> Thread:
        return self._session_cm.session.query(Thread).filter_by(id=thread_id).one_or_none()

    def get_tag_usage_over_time(self):
        # Query to count tag usage over time
        tag_usage = (self._session_cm.session.query(
            Thread.release_date,
            Tag.tag_name,
            func.count(thread_tags.c.tag_name).label('tag_count'))
                     .join(thread_tags, Thread.id == thread_tags.c.thread_id)
                     .join(Tag, thread_tags.c.tag_name == Tag.tag_name)
                     .group_by(Thread.release_date, Tag.tag_name)
                     .order_by(Thread.release_date)
                     .all())

        # Organize data to be used in chart
        tag_data = defaultdict(list)
        for release_date, tag_name, tag_count in tag_usage:
            tag_data[tag_name].append({'date': release_date, 'count': tag_count})

        return tag_data

    def get_threads_by_tag(self, tag_name: str):
        return (self._session_cm.session.query(Thread)
                .join(Thread.tags)
                .filter(Tag.tag_name == tag_name.lower())
                .all())

    def purchase_threads(self, user: User, thread_ids):
        with self._session_cm as scm:
            for thread_id in thread_ids:
                thread = self.find_thread_by_id(thread_id)
                if thread and thread not in user.purchased_threads:
                    user.purchase_thread(thread)
            scm.commit()

    def get_all_tags(self):
        return self._session_cm.session.query(Tag).order_by(Tag.tag_name).all()

    def get_threads_by_tags(self, tag_names):
        normalized_tag_names = [tag_name.lower() for tag_name in tag_names]
        threads = (self._session_cm.session.query(Thread)
                   .join(Thread.tags)
                   .filter(func.lower(Tag.tag_name).in_(normalized_tag_names))
                   .distinct()
                   .all())
        return threads

    def get_recent_threads(self, limit: int = 3) -> list[Thread]:
        return (self._session_cm.session.query(Thread)
                .order_by(Thread.release_date.desc())
                .limit(limit)
                .all())
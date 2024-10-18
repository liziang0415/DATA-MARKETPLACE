import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from threads.addthread_bp import add_thread_bp
from threads.chart_bp import tag_chart_bp
from threads.company_bp import company_bp
from threads.export_data_bp import export_data_bp
from threads.threadDescription_bp import thread_description_bp
from threads.home_bp import home_bp
from threads.threads_bp import threads_bp
from threads.search_bp import search_bp
from threads.login_bp import login_bp
from threads.user_profile_bp import user_profile_bp
from threads.wishlist_bp import wishlist_bp
from threads.adapters.database_repository import SqlAlchemyRepository
from threads.adapters.orm import metadata, map_model_to_tables
import threads.adapters.repository as repo

DATABASE_URI = 'sqlite:///threads.db?check_same_thread=False'

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.Config')

    if test_config is not None:
        app.config.from_mapping(test_config)
    elif app.config['REPOSITORY'] == 'database':
        database_engine = create_engine(DATABASE_URI)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = SqlAlchemyRepository(session_factory)
        clear_mappers()
        map_model_to_tables()

        metadata.create_all(database_engine)

    app.register_blueprint(home_bp)
    app.register_blueprint(threads_bp)
    app.register_blueprint(thread_description_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(user_profile_bp)
    app.register_blueprint(wishlist_bp, url_prefix='/wishlist')
    app.register_blueprint(add_thread_bp)
    app.register_blueprint(tag_chart_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(export_data_bp)
    return app

# __init__.py ________________________________________________________________


"""Initialize Flask app."""

import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy.pool import NullPool

import main.adapters.abstract_repository as repo
from main.adapters import database_repository, memory_repository
from main.adapters.orm import metadata, create_mappers
from main.adapters.services import read_tracks, read_users, read_reviews


def create_app(config=None):
    """Construct the core application."""

    app = Flask(__name__)
    app.config.from_object('config.Config')

    if config:
        app.config.from_mapping(config)

    engine = create_engine(
        'sqlite:///main\\data\\music.db',
        connect_args={'check_same_thread': False},
        poolclass=NullPool
    )
    session = sessionmaker(
        engine,
        autoflush=True,
        autocommit=False
    )

    if app.config['REPOSITORY'] == 'memory':
        print('\n=== MEMORY ===\n')
        
        repo.repo = memory_repository.Repository()

    if app.config['REPOSITORY'] == 'database':
        print('\n=== DATABASE ===\n')

        # reset database
        if app.config['TESTING']:
            print('\n=== DROPPING DATABASE... ===\n')
            metadata.drop_all(engine)
            clear_mappers()

        # reset database tables
        else:
            if os.path.exists('main\\data\\music.db'):
                for table in metadata.sorted_tables:
                    if str(table) == 'reviews':
                        engine.execute(table.delete())

        print('\n=== CREATING DATABASE... ===\n')
        metadata.create_all(engine)
        create_mappers()

        repo.repo = database_repository.Repository(session)

    read_tracks(repo.repo)
    read_users(repo.repo)
    read_reviews(repo.repo)
    print()

    with app.app_context():

        from main.home import home
        app.register_blueprint(home.bp_home)

        from main.auth import auth
        app.register_blueprint(auth.bp_auth)

        from main.browse import browse
        app.register_blueprint(browse.bp_browse)
        app.register_blueprint(browse.bp_track)

        from main.discover import discover
        app.register_blueprint(discover.bp_discover)

        if app.config['REPOSITORY'] == 'database':
            @app.before_request
            def before_flask_http_request_function():
                repo.repo.reset_session()
            
            @app.teardown_appcontext
            def shutdown_session(exception=None):
                repo.repo.close_session()

    return app

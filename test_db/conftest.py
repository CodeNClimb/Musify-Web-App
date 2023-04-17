import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from main.adapters.services import get_project_root

from main.adapters.database_repository import Repository
from main.adapters.orm import metadata, create_mappers


TEST_DATA_PATH_DATABASE_FULL = get_project_root() / "main" / "adapters" / "data"
TEST_DATA_PATH_DATABASE_LIMITED = get_project_root() / "test_db" / "data"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite:///'
TEST_DATABASE_URI_FILE = 'sqlite:///test_db\\data\\music-test.db'

@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    create_mappers()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = Repository(session_factory)
    database_mode = True
    yield engine
    metadata.drop_all(engine)


@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    create_mappers()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = Repository(session_factory)
    database_mode = True
    yield session_factory
    metadata.drop_all(engine)


@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    create_mappers()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)
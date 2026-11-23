from functools import lru_cache

from app.database import get_engine, get_session_factory


@lru_cache(maxsize=1)
def _session_factory():
    return get_session_factory(get_engine())


def get_db():
    db = _session_factory()()
    try:
        yield db
    finally:
        db.close()

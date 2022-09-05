from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from milkrage.config import Config


def get_dsn(cfg: Config = Config()):
    return (
        f"{cfg.db_driver}://{cfg.db_username}:{cfg.db_password}"
        f"@{cfg.db_host}:{cfg.db_port}/{cfg.db_name}"
    )


def get_engine():
    return create_engine(get_dsn())


def get_session():
    session: Session = SessionDB()

    try:
        yield session
    finally:
        session.close()


SessionDB = sessionmaker(bind=get_engine(), autoflush=False)

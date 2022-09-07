import os

from pydantic import BaseSettings


def get_dir(relative_path: str = "") -> str:
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), relative_path)
    )


class Config(BaseSettings):
    templates_path: str = get_dir("templates")
    static_path: str = get_dir("static")

    db_driver: str = "mysql+pymysql"
    db_host: str = "127.0.0.1"
    db_port: str = "3306"
    db_username: str = "root"
    db_password: str = "mysql"
    db_name: str = "milkrage"
    db_pool_recycle: int = 3600

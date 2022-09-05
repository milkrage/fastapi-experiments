from sqlalchemy import Column, DateTime, Integer, String, Table, Text
from sqlalchemy import ForeignKey, desc, select
from sqlalchemy.orm import Session, declarative_base, relationship
from sqlalchemy.sql import func

BaseModel = declarative_base()


class ModelMixin:
    create_at = Column(DateTime, server_default=func.now())
    update_at = Column(DateTime, server_onupdate=func.now())

    @classmethod
    def list(cls, session: Session):
        return session.scalars(select(cls).order_by(desc(cls.create_at))).all()


tags_posts = Table(
    "tags_posts",
    BaseModel.metadata,
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
)


class Post(BaseModel, ModelMixin):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    body = Column(Text, nullable=False)

    tags = relationship("Tag", secondary="tags_posts", back_populates="posts")

    @staticmethod
    def list_by_tag(tag: str, session: Session):
        return session.scalars(
            select(Post).join(tags_posts).join(Tag).where(Tag.title == tag)
        ).all()

    @staticmethod
    def get_by_id(id: int, session: Session):
        return session.scalar(select(Post).where(Post.id == id))


class Tag(BaseModel, ModelMixin):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False, unique=True)

    posts = relationship("Post", secondary="tags_posts", back_populates="tags")

    @staticmethod
    def list_order_by_posts(session: Session):
        return session.execute(
            select(Tag.id, Tag.title, func.count(Tag.id))
            .join(tags_posts)
            .group_by(Tag.id)
            .order_by(desc(func.count(Tag.id)))
        ).all()

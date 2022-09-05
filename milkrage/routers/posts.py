from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from milkrage.config import Config
from milkrage.database import get_session
from milkrage.database.models import Post

config = Config()
router = APIRouter()
template = Jinja2Templates(config.templates_path)


@router.get("/", name="get_posts")
def get_posts(request: Request, session: Session = Depends(get_session)):
    posts: list[Post] = Post.list(session)

    if not posts:
        raise HTTPException(status_code=404)

    return template.TemplateResponse(
        "posts/list.html",
        {"request": request, "posts": posts, "title": "Posts"},
    )


@router.get("/{id}", name="get_post_by_id")
def get_post_by_id(
    request: Request,
    id: int,
    session: Session = Depends(get_session),
):
    post: Post = Post.get_by_id(id, session)

    if not post:
        raise HTTPException(status_code=404)

    return template.TemplateResponse(
        "posts/item.html",
        {"request": request, "post": post, "title": post.title},
    )

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from milkrage.config import Config
from milkrage.database import get_session
from milkrage.database.models import Post, Tag

config = Config()
router = APIRouter()
template = Jinja2Templates(config.templates_path)


@router.get("/", name="get_tags")
def get_tags(request: Request, session: Session = Depends(get_session)):
    tags: list[Tag] = Tag.list_order_by_posts(session)

    if not tags:
        raise HTTPException(status_code=404)

    return template.TemplateResponse(
        "tags/list.html",
        {"request": request, "tags": tags, "title": "Tags"},
    )


@router.get("/{tag}", name="get_posts_by_tag")
def get_posts_by_tag(
    request: Request,
    tag: str,
    session: Session = Depends(get_session),
):
    posts: list[Post] = Post.list_by_tag(tag, session)

    if not posts:
        raise HTTPException(status_code=404)

    return template.TemplateResponse(
        "posts/list.html",
        {"request": request, "posts": posts, "title": f"Tag: {tag}"},
    )

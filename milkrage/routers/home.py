from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from milkrage.config import Config

config = Config()
router = APIRouter()
template = Jinja2Templates(config.templates_path)


@router.get("/", name="home")
def homepage(request: Request):
    return template.TemplateResponse("home.html", context={"request": request})

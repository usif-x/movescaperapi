from fastapi import Depends
from fastapi.routing import APIRouter

from app.service.arabseed import ArabSeedService


def get_arab_seed_service() -> ArabSeedService:
    return ArabSeedService()


router = APIRouter(
    prefix="/arabseed",
    tags=["ArabSeed"],
)


@router.get("/films")
async def get_films_from_films_page(
    service: ArabSeedService = Depends(get_arab_seed_service),
):
    films = service.fetch_films_from_films_page()
    return {"films": films}


@router.get("/home/films")
async def get_films_from_home(
    service: ArabSeedService = Depends(get_arab_seed_service),
):
    films = service.fetch_films_from_home()
    return {"films": films}


@router.get("/films/netflix")
async def get_netflix_films(
    page: int = 1,
    service: ArabSeedService = Depends(get_arab_seed_service),
):
    films = service.fetch_netflix_films(page=page)
    return {"films": films}


@router.get("/films/{url:path}")
async def get_film_information(
    url: str,
    service: ArabSeedService = Depends(get_arab_seed_service),
):
    film_info = service.fetch_film_information(url)
    return film_info

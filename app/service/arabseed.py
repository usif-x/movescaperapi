from app.helper.arabseed import (
    get_film_information,
    get_films_data_from_home,
    get_films_from_films_page,
    get_netflix_films,
)


class ArabSeedService:
    @staticmethod
    def __init__():
        pass

    def fetch_film_information(self, url):
        return get_film_information(url)

    def fetch_films_from_home(self):
        return get_films_data_from_home()

    def fetch_films_from_films_page(self):
        return get_films_from_films_page()

    def fetch_netflix_films(self, page=1):
        return get_netflix_films(page=page)

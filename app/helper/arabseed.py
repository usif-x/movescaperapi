import json

import bs4
import requests

from app.core.config import get_arabseed_endpoints

arabseed_settings = get_arabseed_endpoints()


def get_home_page_content():
    response = requests.get(arabseed_settings.URL + arabseed_settings.HOME)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    # Parse the content here if needed, but for now, return soup or something
    return soup


def get_film_information(url):
    # Validate URL
    if not url:
        raise ValueError("URL parameter is required")

    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError(
            f"Invalid URL: '{url}'. URL must start with http:// or https://"
        )

    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, "html.parser")

    film_info = {}
    single_area = soup.find("section", class_="single__area")
    if not single_area:
        return None

    # Cover image
    cover_img = single_area.find("div", class_="single__cover").find("img")
    film_info["cover_image"] = cover_img.get("src") if cover_img else None

    # User actions (likes and views)
    user_actions = single_area.find("div", class_="user__actions")
    if user_actions:
        likes_btn = user_actions.find("button", id="like__post")
        views_count = user_actions.find("button", class_="views__count")
        film_info["user_actions"] = {
            "likes": (
                likes_btn.find("span", class_="like__count").text.strip()
                if likes_btn
                else None
            ),
            "views": (
                views_count.find("span", class_="like__count").text.strip()
                if views_count
                else None
            ),
        }

    # Title
    title_h1 = single_area.find("h1", class_="post__name")
    film_info["title"] = title_h1.text.strip() if title_h1 else None

    # Breadcrumbs
    breadcrumbs_ol = single_area.find("ol", class_="bread__crumbs")
    if breadcrumbs_ol:
        film_info["breadcrumbs"] = [
            li.text.strip() for li in breadcrumbs_ol.find_all("li")
        ]

    # IMDB Rating
    rating_box = single_area.find("div", class_="rating__box")
    if rating_box:
        rate_txt = rating_box.find("div", class_="rate__txt")
        votes_span = rating_box.find("span", class_="votes")
        film_info["imdb_rating"] = {
            "rating": rate_txt.text.strip() if rate_txt else None,
            "votes": votes_span.text.strip() if votes_span else None,
        }

    # Description and Story
    film_info["description"] = single_area.find(
        "p", class_="post__content"
    ).text.strip()
    story_div = single_area.find("div", class_="post__story")
    film_info["story"] = story_div.text.strip() if story_div else None

    # Details
    details = {}
    info_area_ul = single_area.find("ul", class_="info__area__ul")
    if info_area_ul:
        for li in info_area_ul.find_all("li"):
            title_kit = li.find("div", class_="title__kit")
            if title_kit:
                key = title_kit.find("span").text.strip().replace(":", "").strip()
                value_tags = li.find("ul", class_="tags__list")
                if value_tags:
                    details[key] = [a.text.strip() for a in value_tags.find_all("a")]
                else:
                    value_a = li.find("a")
                    if value_a:
                        details[key] = value_a.text.strip()
    film_info["details"] = details

    # Watch and download links
    watch_btn = single_area.find("a", class_="watch__btn")
    download_btn = single_area.find("a", class_="download__btn")
    film_info["links"] = {
        "watch": watch_btn.get("href") if watch_btn else None,
        "download": download_btn.get("href") if download_btn else None,
    }

    # Poster image
    poster_side = single_area.find("div", class_="poster__side")
    poster_img = None
    if poster_side:
        poster_single = poster_side.find("div", class_="poster__single")
        if poster_single:
            # Find the first img tag directly (not checking for trailer)
            poster_img = poster_single.find("img", class_="images__loader")
            # If not found with class, try without class filter
            if not poster_img:
                poster_img = poster_single.find("img")

    film_info["poster_image"] = (
        poster_img.get("src") or poster_img.get("data-src") if poster_img else None
    )

    # Quality ribbon
    if poster_side:
        ribbon = poster_side.find("div", class_="ribbon")
        film_info["quality"] = ribbon.text.strip() if ribbon else None

    # Visitor rating
    star_rating = single_area.find("div", class_="star__rating")
    if star_rating:
        avg_span = star_rating.find("span", class_="rating-average")
        count_span = star_rating.find("span", class_="rating-count")
        film_info["visitor_rating"] = {
            "average": avg_span.text.strip() if avg_span else None,
            "count": count_span.text.strip() if count_span else None,
        }

    return film_info


def get_films_data_from_home():
    response = requests.get(arabseed_settings.URL + arabseed_settings.HOME)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    episodes = []
    for item in soup.find_all("a", class_="episode__item"):
        url = item.get("href")
        title_attr = item.get("title")
        img = item.find("img")
        image = img.get("data-src") if img else None
        is_last = bool(item.find("div", class_="ribbon__new"))
        title_span = item.find("span")
        series_title = title_span.text.strip() if title_span else None
        episode_p = item.find("p")
        episode_text = episode_p.text.strip() if episode_p else None
        episode_em = item.find("em")
        episode_number = episode_em.text.strip() if episode_em else None
        episodes.append(
            {
                "url": url,
                "title": title_attr,
                "image": image,
                "is_last": is_last,
                "series_title": series_title,
                "episode_text": episode_text,
                "episode_number": episode_number,
            }
        )
    return episodes


def get_films_from_films_page():
    response = requests.get(arabseed_settings.URL + arabseed_settings.FILMS)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    films = []

    # Handle slider__single cards
    for item in soup.find_all("div", class_="slider__single"):
        a_tag = item.find("a")
        if not a_tag:
            continue

        url = a_tag.get("href")
        title = a_tag.get("title")

        post_image_div = a_tag.find("div", class_="post__image")
        img = post_image_div.find("img") if post_image_div else None
        # Try src first, then data-src for lazy-loaded images
        image = None
        if img:
            image = img.get("src") or img.get("data-src")

        ratings_div = a_tag.find("div", class_="post__ratings")
        ratings = ratings_div.text.strip() if ratings_div else None

        category_div = a_tag.find("div", class_="post__category")
        category = category_div.text.strip() if category_div else None

        post_info = a_tag.find("div", class_="post__info")
        info_h3 = post_info.find("h3") if post_info else None
        info_title = info_h3.text.strip() if info_h3 else None

        genres = []
        if post_info:
            genres = [
                li.text.strip() for li in post_info.find_all("li", class_="__genre")
            ]

        runtime_li = post_info.find("li", class_="__runtime") if post_info else None
        runtime = runtime_li.text.strip() if runtime_li else None

        post_content = a_tag.find("div", class_="post__content")
        description_p = post_content.find("p") if post_content else None
        description = description_p.text.strip() if description_p else None

        trailer_btn = a_tag.find("div", class_="trailer__btn")
        trailer = trailer_btn.get("data-iframe") if trailer_btn else None

        films.append(
            {
                "url": url,
                "title": title,
                "image": image,
                "ratings": ratings,
                "category": category,
                "info": {
                    "title": info_title,
                    "genres": genres,
                    "runtime": runtime,
                },
                "description": description,
                "trailer": trailer,
            }
        )

    # Handle item__contents cards
    for item in soup.find_all("div", class_="item__contents"):
        a_tag = item.find("a", class_="movie__block")
        if not a_tag:
            continue

        url = a_tag.get("href")
        title = a_tag.get("title")

        post_image_div = a_tag.find("div", class_="post__image")
        img = post_image_div.find("img") if post_image_div else None
        # Try src first, then data-src for lazy-loaded images
        image = None
        if img:
            image = img.get("src") or img.get("data-src")

        category_div = a_tag.find("div", class_="post__category")
        category = category_div.text.strip() if category_div else None

        quality_div = a_tag.find("div", class_="__quality")
        quality = quality_div.text.strip() if quality_div else None

        post_info = a_tag.find("div", class_="post__info")
        description = None
        info_title = None
        if post_info:
            description_p = post_info.find("p")
            description = description_p.text.strip() if description_p else None
            info_h3 = post_info.find("h3")
            info_title = info_h3.text.strip() if info_h3 else None

        films.append(
            {
                "url": url,
                "title": title,
                "image": image,
                "ratings": None,  # Not available in this card type
                "category": category,
                "info": {
                    "title": info_title,
                    "genres": [quality] if quality else [],  # Using quality as a genre
                    "runtime": None,  # Not available
                },
                "description": description,
                "trailer": None,  # Not available
            }
        )
    return films


def get_items_from_box_items(page=1, endpoint=None):
    if not endpoint:
        raise ValueError("endpoint parameter is required")

    # Ensure endpoint starts with /
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    url = arabseed_settings.URL + endpoint
    if page > 1:
        url += f"/page/{page}/"

    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    films = []

    # Handle box items (li with box classes)
    for item in soup.find_all("li", class_="box__xs__2"):
        item_contents = item.find("div", class_="item__contents")
        if not item_contents:
            continue

        a_tag = item_contents.find("a", class_="movie__block")
        if not a_tag:
            continue

        url_film = a_tag.get("href")
        title = a_tag.get("title")

        post_image_div = a_tag.find("div", class_="post__image")
        img = post_image_div.find("img") if post_image_div else None
        # Try src first, then data-src for lazy-loaded images
        image = None
        if img:
            image = img.get("src") or img.get("data-src")

        category_div = a_tag.find("div", class_="post__category")
        category = category_div.text.strip() if category_div else None

        genre_div = a_tag.find("div", class_="__genre")
        genre = genre_div.text.strip() if genre_div else None

        ratings_div = a_tag.find("div", class_="post__ratings")
        ratings = ratings_div.text.strip() if ratings_div else None

        quality_div = a_tag.find("div", class_="__quality")
        quality = quality_div.text.strip() if quality_div else None

        post_info = a_tag.find("div", class_="post__info")
        description = None
        info_title = None
        if post_info:
            description_p = post_info.find("p")
            description = description_p.text.strip() if description_p else None
            info_h3 = post_info.find("h3")
            info_title = info_h3.text.strip() if info_h3 else None

        films.append(
            {
                "url": url_film,
                "title": title,
                "image": image,
                "ratings": ratings,
                "category": category,
                "info": {
                    "title": info_title,
                    "genres": [g for g in [genre, quality] if g],
                    "runtime": None,  # Not available in this card type
                },
                "description": description,
                "trailer": None,  # Not available
            }
        )

    # Extract pagination information
    pagination_info = {
        "current_page": page,
        "next_page": None,
        "prev_page": None,
        "last_page": None,
        "total_pages": None,
        "has_next": False,
        "has_prev": False,
    }

    pagination_ul = soup.find("ul", class_="page-numbers")
    if pagination_ul:
        # Get current page
        current_span = pagination_ul.find("span", class_="current")
        if current_span:
            try:
                pagination_info["current_page"] = int(current_span.text.strip())
            except ValueError:
                pass

        # Get next page
        next_link = pagination_ul.find("a", class_="next")
        if next_link:
            pagination_info["has_next"] = True
            pagination_info["next_page"] = pagination_info["current_page"] + 1

        # Get prev page
        prev_link = pagination_ul.find("a", class_="prev")
        if prev_link:
            pagination_info["has_prev"] = True
            pagination_info["prev_page"] = pagination_info["current_page"] - 1

        # Get all page numbers to find the last page
        page_links = pagination_ul.find_all("a", class_="page-numbers")
        page_numbers = []
        for link in page_links:
            if link.get("class") and (
                "next" in link.get("class") or "prev" in link.get("class")
            ):
                continue
            try:
                page_num = int(link.text.strip())
                page_numbers.append(page_num)
            except ValueError:
                continue

        if page_numbers:
            pagination_info["last_page"] = max(page_numbers)
            pagination_info["total_pages"] = max(page_numbers)

    return {
        "films": films,
        "pagination": pagination_info,
        "total_results": len(films),
    }


def get_netflix_films(page=1):
    return get_items_from_box_items(page=page, endpoint=arabseed_settings.NETFLIX_FILMS)

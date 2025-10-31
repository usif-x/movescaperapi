# Move Scraper API

A powerful web scraping API for movie and TV show content from ArabSeed and other streaming sites.

## 🎬 Overview

Move Scraper API is a FastAPI-based web scraping service that extracts movie and TV show information from various streaming platforms. Currently supports ArabSeed with more sites coming soon.

## ✨ Features

- **Film Information Extraction**: Get detailed information about movies and TV shows
- **Pagination Support**: Navigate through multiple pages of content
- **Multiple Card Layouts**: Supports various content card formats (slider, grid, box items)
- **Episode Tracking**: Track latest episodes and series information
- **Netflix Content**: Dedicated endpoint for Netflix films
- **IMDB Ratings**: Extract IMDB ratings and vote counts
- **Visitor Ratings**: Get site visitor ratings and reviews
- **Download & Watch Links**: Direct links to watch or download content
- **Comprehensive Metadata**: Genres, quality, runtime, release year, and more

## 🚀 API Endpoints

### Films

#### Get Films from Home Page

```
GET /api/films/home
```

Returns latest episodes and films from the home page.

#### Get Films from Films Page

```
GET /api/films
```

Returns all films from the films page with support for slider and grid layouts.

#### Get Netflix Films

```
GET /api/films/netflix?page=1
```

Returns Netflix films with pagination support.

**Query Parameters:**

- `page` (optional): Page number (default: 1)

**Response:**

```json
{
  "films": [...],
  "pagination": {
    "current_page": 1,
    "next_page": 2,
    "prev_page": null,
    "last_page": 28,
    "total_pages": 28,
    "has_next": true,
    "has_prev": false
  },
  "total_results": 24
}
```

#### Get Film Information

```
GET /api/film?url=https://example.com/film-url
```

Returns detailed information about a specific film.

**Query Parameters:**

- `url` (required): Full URL of the film page

**Response:**

```json
{
  "cover_image": "https://...",
  "poster_image": "https://...",
  "title": "Film Title",
  "description": "Film description...",
  "story": "Detailed plot...",
  "imdb_rating": {
    "rating": "7.5 / 10",
    "votes": "1234 votes"
  },
  "visitor_rating": {
    "average": "8 / 10",
    "count": "( 56 votes )"
  },
  "user_actions": {
    "likes": "123",
    "views": "4567"
  },
  "details": {
    "Category": ["Action", "Drama"],
    "Genre": ["Thriller"],
    "Duration": "2 hours 15 minutes",
    "Year": ["2025"],
    "Quality": ["WEB-DL"],
    "Country": ["USA"]
  },
  "links": {
    "watch": "https://.../watch/",
    "download": "https://.../download/"
  },
  "quality": "WEB-DL",
  "breadcrumbs": [...]
}
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:

```bash
git clone https://github.com/usif-x/movescaperapi.git
cd arabseed
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure settings in `app/core/config.py`

5. Run the server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🏗️ Project Structure

```
arabseed/
├── app/
│   ├── core/
│   │   └── config.py          # Configuration settings
│   ├── helper/
│   │   ├── arabseed.py        # Web scraping functions
│   │   └── home.py            # Home page helpers
│   ├── router/
│   │   ├── __init__.py
│   │   └── arabseed.py        # API route handlers
│   ├── service/
│   │   └── arabseed.py        # Business logic layer
│   └── template/              # HTML templates
├── main.py                     # FastAPI application entry point
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 Configuration

Edit `app/core/config.py` to configure:

- Base URL for ArabSeed
- API endpoints
- Scraping settings

## 📦 Dependencies

- **FastAPI**: Modern web framework for building APIs
- **BeautifulSoup4**: HTML parsing and web scraping
- **Requests**: HTTP library for making requests
- **Uvicorn**: ASGI server for running the application

## 🌟 Features in Detail

### Pagination Support

All list endpoints support pagination with comprehensive metadata:

- Current page number
- Next/Previous page numbers
- Total pages
- Navigation flags

### Multiple Layout Support

The scraper handles different content layouts:

- **Slider Cards**: Featured content carousels
- **Grid Items**: Standard grid layout
- **Box Items**: Detailed box layout with ratings

### Error Handling

- URL validation
- Missing data handling
- Graceful fallbacks for optional fields

## 🚧 Upcoming Features

- Support for additional streaming sites
- Advanced filtering and search
- Caching layer for improved performance
- Rate limiting
- Authentication
- Webhook notifications for new content

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is for educational purposes only. Please respect the terms of service of the websites you scrape.

## ⚠️ Disclaimer

This tool is intended for educational and personal use only. Be respectful of website terms of service and implement appropriate rate limiting. The authors are not responsible for misuse of this software.

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Note**: More sites will be added soon! Stay tuned for updates.

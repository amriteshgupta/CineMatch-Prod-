import random
import requests
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# TMDb API Key
API_KEY = 'd232dfe0f5fd89f13c62ec0494f65c84'
BASE_URL = 'https://api.themoviedb.org/3'

# Set up Jinja2 template directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def random_movie(request: Request, year: int = Query(None, ge=1900), genre: str = None):
    # Construct the API URL with optional filters
    api_url = f"{BASE_URL}/discover/movie?api_key={API_KEY}"

    # Add year and genre filters if provided
    if year:
        api_url += f"&primary_release_year={year}"
    if genre:
        api_url += f"&with_genres={genre}"

    # Fetch the movie data
    response = requests.get(api_url)
    movie_data = response.json()

    # Pick a random movie from the filtered list
    if movie_data['results']:
        random_movie = random.choice(movie_data['results'])
    else:
        random_movie = {
            "title": "No movies found",
            "overview": "Try different filters.",
            "release_date": "N/A",
            "poster_path": ""
        }

    # Pass movie details to the template
    return templates.TemplateResponse("movie.html", {
        "request": request,
        "title": random_movie['title'],
        "overview": random_movie['overview'],
        "release_date": random_movie['release_date'],
        "poster_path": f"https://image.tmdb.org/t/p/w500{random_movie['poster_path']}" if random_movie['poster_path'] else ""
    })

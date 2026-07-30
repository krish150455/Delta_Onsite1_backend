from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
import httpx
from dotenv import load_dotenv
from schemas import SearchRequest,SearchResponse,MovieRequest,MovieResponse, FavoriteRequest
from database import get_connection,create_tables

load_dotenv()

app = FastAPI()
create_tables()

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
BACKDROP_BASE = "https://image.tmdb.org/t/p/original"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('TMDB_TOKEN')}",
    "accept": "application/json"
}

@app.post("/movies/search", response_model=list[SearchResponse])
async def search_movies(request: SearchRequest):
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL + "/search/movie",headers=HEADERS,params={"query": request.query})

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()
        )
    
    data = response.json()
    listie=[]
    for movie in data["results"]:
        listie.append(SearchResponse(
                    id=movie["id"],
                    title=movie["title"],
                    release_date=movie["release_date"],
                    rating=movie["vote_average"],
                    poster=IMAGE_BASE + movie["poster_path"]
                    if movie["poster_path"] else None
                ))
    return listie

@app.post("/movies/details", response_model=MovieResponse)
async def movie_details(request: MovieRequest):
    async with httpx.AsyncClient() as client:

        response = await client.get(
            BASE_URL + f"/movie/{request.movie_id}",
            headers=HEADERS
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()
        )

    movie = response.json()

    return MovieResponse(
        id=movie["id"],
        title=movie["title"],
        overview=movie["overview"],
        runtime=movie["runtime"],
        release_date=movie["release_date"],
        rating=movie["vote_average"],
        genre=movie["genres"][0]["name"],
        poster=IMAGE_BASE + movie["poster_path"]
        if movie["poster_path"] else None,
        backdrop=BACKDROP_BASE + movie["backdrop_path"]
        if movie["backdrop_path"] else None
    )

@app.post("/movies/favorite")
async def mark_favorite(request: FavoriteRequest):
    conn=get_connection()
    cursor=conn.cursor()
    try:
        cursor.execute("""INSERT INTO favorite_movies VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT(id) DO NOTHING""",
                       (request.id,request.title,request.overview,request.runtime,request.release_date,request.rating,
                        request.genre,request.poster,request.backdrop,request.is_favorite) )
        conn.commit()
        return {
    "message": "Movie added to favorites"
}
    finally:
        if conn:
            cursor.close()
            conn.close()

@app.get("/movies/favorites",response_model=list[FavoriteRequest])
async def get_favorites():
    conn=get_connection()
    cursor=conn.cursor()
    try:
        listie=[]
        cursor.execute("""SELECT * FROM favorite_movies""")
        response=cursor.fetchall()
        for each in response:
            listie.append(FavoriteRequest(
                id=each[0],
                title=each[1],
                overview=each[2],
                runtime=each[3],
                release_date=each[4],
                rating=each[5],
                genre=each[6],
                poster=each[7],
                backdrop=each[8],
                is_favorite=each[9]
            ))
        return listie
    finally:
        if conn:
            cursor.close()
            conn.close()
from pydantic import BaseModel
from typing import Optional,List

class SearchRequest(BaseModel):
    query:str

class SearchResponse(BaseModel):
    id: int
    title: str
    release_date: str
    rating: float
    poster:Optional[str] = None

class MovieRequest(BaseModel):
    movie_id:int

class MovieResponse(BaseModel):
    id: int
    title: str
    overview: str
    runtime: int
    release_date: str
    rating: float
    genre: str
    poster: Optional[str] = None
    backdrop: Optional[str] = None

class FavoriteRequest(BaseModel):
        id: int
        title: str
        overview: str
        runtime: int
        release_date: str
        rating: float
        genre: str
        poster: Optional[str] = None
        backdrop: Optional[str] = None
        is_favorite: bool
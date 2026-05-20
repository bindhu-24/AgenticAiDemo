from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
# from app.db import engine, Base
# from app import models  # import models so Base knows about them

app = FastAPI(title="Books API", version="0.0.1")

@app.on_event("startup")
async def startup():
    # Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

@app.get('/', tags=["home"])
def message():
    return {"status":"ok"}

books = [
        {'id': 1,
        'title': 'Harry Potter',
        'author': 'J.K. Rowling',
        'year': 1997,
        'category': 'Fantasy',
        'available_copies': 5,
        'price': 499},
        {'id': 2,
        'title': 'Atomic Habits',
        'author': 'James Clear',
        'year': 2018,
        'category': 'Self Help',
        'available_copies': 8,
        'price': 359},
        {'id': 3,
        'title': 'Malgudi Days',
        'author': 'R.K. Narayan',
        'year': 1943,
        'category': 'Fiction',
        'available_copies': 3,
        'price': 195}]

@app.get('/books',tags=['books'])
def get_books():
    return books

@app.get('/books/{book_id}', tags=['books'])
def get_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            return book
    return {'message': 'Book not found'}

@app.get('/books/category/{category}', tags=['books'])
def get_books_by_category(category: str):
    category_books = [book for book in books if book['category'].lower() == category.lower()]
    return category_books

from fastapi import Body
@app.post('/books',tags=['books'])
def create_book(
    id:int = Body(...),
    title: str= Body(...),
    author: str=Body(...),
    year: int=Body(...),
    available_copies: int=Body(...),
    category: str=Body(...),
    price: int=Body(...)
):
    new_book = {'id':id, 'title':title, 'year':year, 'category':category, 'author':author,'available_copies':available_copies,'price':price}
    books.append(new_book)
    return new_book

from pydantic import BaseModel, Field
from typing import Optional

class Book(BaseModel):
    id: int = Field(..., example=4)
    title: str = Field(min_length=2, max_length=100, example='Harry Porter')
    author: str = Field(min_length=3, max_length=50, example='J.K. Rowling')
    category: str = Field(..., example='Fantasy')
    year: int = Field(...,ge=1900, le=2026, example=1997)
    available_copies: int = Field(...,ge=0,example=5)
    price:int = Field(...,ge=0 ,example=499)

@app.put('/books/{book_id}', tags=['books'])
def update_book(book_id: int, book:Book):
    for index, existing_book in enumerate(books):
        if existing_book['id'] == book_id:
            books[index] = book.dict()
            return books[index]
    return {'message': 'Book not found'}
    
@app.delete('/books/{book_id}', tags=['books'])
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book['id'] == book_id:
            deleted_book = books.pop(index)
            return {'message': 'Book Deleted', 'book': deleted_book}
    return {'message': 'Book not found'}
    

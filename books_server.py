from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI(
    title="Books Server",
    description="A simple book management server with categories",
    version="1.1.0",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for books
library: Dict[int, Dict[str, str]] = {}


class Book(BaseModel):
    title: str
    author: str
    category: Optional[str] = None  # New field


class BookResponse(Book):
    id: int


def get_book_by_id(book_id: int) -> Dict[str, str]:
    book = library.get(book_id)
    if not book:
        raise HTTPException(
            status_code=404, detail=f"Book with ID {book_id} not found."
        )
    return book


@app.post("/books", response_model=Dict[str, str], operation_id="add_book")
async def add_book(book: Book = Body(...)):
    if not book.title.strip() or not book.author.strip():
        raise HTTPException(
            status_code=400, detail="Title and author must be non-empty."
        )

    book_id = len(library) + 1
    library[book_id] = {
        "title": book.title.strip(),
        "author": book.author.strip(),
        "category": book.category.strip().lower() if book.category else None,
    }
    return {"message": f"Book added successfully with ID {book_id}"}


@app.get("/books", response_model=List[BookResponse], operation_id="get_all_books")
async def get_all_books():
    return [{"id": book_id, **book} for book_id, book in library.items()]


@app.get("/books/id/{book_id}", response_model=BookResponse, operation_id="get_book")
async def get_book(book_id: int):
    book = get_book_by_id(book_id)
    return {"id": book_id, **book}


@app.delete(
    "/books/id/{book_id}", response_model=Dict[str, str], operation_id="delete_book"
)
async def delete_book(book_id: int):
    get_book_by_id(book_id)
    del library[book_id]
    return {"message": f"Book with ID {book_id} removed successfully."}


@app.get(
    "/books/search", response_model=List[BookResponse], operation_id="search_books"
)
async def search_books(
    author: Optional[str] = Query(None, description="Search by author"),
    title: Optional[str] = Query(None, description="Search by title"),
    category: Optional[str] = Query(None, description="Search by category"),
):
    if not (author or title or category):
        raise HTTPException(
            status_code=400,
            detail="At least one of 'author', 'title', or 'category' must be provided.",
        )

    query_category = category.strip().lower() if category else None

    results = [
        {"id": book_id, **book}
        for book_id, book in library.items()
        if (author and author.lower() in book["author"].lower())
        or (title and title.lower() in book["title"].lower())
        or (query_category and book.get("category") == query_category)
    ]
    return results


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)

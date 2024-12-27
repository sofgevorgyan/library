
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

@app.post("/books/")
def create_book(title: str, author: str, publication_year: int, db: Session = Depends(database.SessionLocal)):
    return crud.create_book(db=db, title=title, author=author, publication_year=publication_year)

@app.get("/books/")
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(database.SessionLocal)):
    return crud.get_books(db=db, skip=skip, limit=limit)

@app.post("/readers/")
def create_reader(name: str, email: str, db: Session = Depends(database.SessionLocal)):
    return crud.create_reader(db=db, name=name, email=email)

@app.get("/readers/")
def get_readers(skip: int = 0, limit: int = 10, db: Session = Depends(database.SessionLocal)):
    return crud.get_readers(db=db, skip=skip, limit=limit)

@app.post("/loans/")
def create_loan(book_id: int, reader_id: int, loan_date: str, return_date: str, db: Session = Depends(database.SessionLocal)):
    return crud.create_loan(db=db, book_id=book_id, reader_id=reader_id, loan_date=loan_date, return_date=return_date)

@app.get("/loans/")
def get_loans(skip: int = 0, limit: int = 10, db: Session = Depends(database.SessionLocal)):
    return crud.get_loans(db=db, skip=skip, limit=limit)

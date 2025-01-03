from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exc
from models import SessionLocal, Book
from schemas import BookCreate, BookSchema, ReaderCreate, ReaderSchema, BorrowCreate,  BorrowSchema

app = FastAPI()

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create - создание новой книги
@app.post("/books/", response_model=BookSchema)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(
        title=book.title,
        publishing_hous=book.publishing_hous, 
        author=book.author,
        publication_date=book.publication_date,
        genre=book.genre)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Read - получение списка всех книг
@app.get("/books/", response_model=list[BookSchema])
def get_books(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    books = db.query(Book).offset(skip).limit(limit).all()
    return books

# Read - получение книги по ID
@app.get("/books/{book_id}", response_model=BookSchema)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# Update - обновление данных книги
@app.put("/books/{book_id}", response_model=BookSchema)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db_book.title = book.title
    db_book.author = book.author
    db_book.description = book.description
    
    db.commit()
    db.refresh(db_book)
    return db_book

# Delete - удаление книги
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}


@app.post("/readers/",response_model=ReaderSchema)
def create_reader(reader: ReaderCreate, db:Session=Depends(get_db)):
    db_reader=Reader(
        name=reader.name,
        phone=reader.phone, 
        address=reader.address,
        passport_number=reader.passport_number
    )
    try:
        db.add(db_reader)
        db.commit()
        db.refresh(db_reader)
    except exc.lntegerrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
        return db_reader

@app.get("/readers/", response_model=list[ReaderSchema])
def get_readers(db: Session = Depends(get_db)):
    return db.query(Reader).all()

@app.get("/readers/{reader_id}", response_model=ReaderSchema)
def get_reader(reader_id: int, db: Session = Depends(get_db)):
    db_reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not db_reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return db_reader

@app.put("/readers/{reader_id}", response_model=ReaderSchema)
def update_reader(reader_id: int, reader: ReaderCreate, db: Session = Depends(get_db)):
    db_reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not db_reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    db_reader.name = reader.name
    db_reader.phone = reader.phone
    db_reader.address = reader.address
    db.commit()
    db.refresh(db_reader)
    return db_reader

@app.delete("/readers/{reader_id}")
def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    db_reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not db_reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    db.delete(db_reader)
    db.commit()
    return {"message": "Reader deleted successfully"}


@app.post("/borrows/", response_model=BorrowSchema)
def create_borrow(borrow: BorrowCreate, db: Session = Depends(get_db)):
    db_borrow = Borrow(
        book_id=borrow.book_id,
        reader_id=borrow.reader_id,
        borrow_date=borrow.borrow_date,
        return_date=borrow.return_date,
        deadline=borrow.deadline
    )
    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)
    return db_borrow

@app.get("/borrows/", response_model=list[BorrowSchema])
def get_borrows(db: Session = Depends(get_db)):
    return db.query(Borrow).all()

@app.get("/borrows/{borrow_id}", response_model=BorrowSchema)
def get_borrow(borrow_id: int, db: Session = Depends(get_db)):
    db_borrow = db.query(Borrow).filter(Borrow.id == borrow_id).first()
    if not db_borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    return db_borrow

@app.put("/borrows/{borrow_id}", response_model=BorrowSchema)
def update_borrow(borrow_id: int, borrow: BorrowCreate, db: Session = Depends(get_db)):
    db_borrow = db.query(Borrow).filter(Borrow.id == borrow_id).first()
    if not db_borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    db_borrow.book_id = borrow.book_id
    db_borrow.reader_id = borrow.reader_id
    db_borrow.borrow_date = borrow.borrow_date
    db_borrow.return_date = borrow.return_date
    db.commit()
    db.refresh(db_borrow)
    return db_borrow

@app.delete("/borrows/{borrow_id}")
def delete_borrow(borrow_id: int, db: Session = Depends(get_db)):
    db_borrow = db.query(Borrow).filter(Borrow.id == borrow_id).first()
    if not db_borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    db.delete(db_borrow)
    db.commit()
    return {"message": "Borrow record deleted successfully"}
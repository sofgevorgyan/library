from pydantic import BaseModel
from datetime import date

# Модель книги для входных и выходных данных
class BookBase(BaseModel):
    title: str
    author: str
    description: str

class BookCreate(BookBase):
    pass

class BookSchema(BookBase):
    id: int

    class Config:
        orm_mode = True

class ReaderBase(BaseModel):
    name: str
    phone: int
    address: str

class ReaderCreate(ReaderBase):
    pass

class ReaderSchema(ReaderBase):
    id: int

    class Config:
        orm_mode = True

class BorrowBase(BaseModel):
    book_id: int
    reader_id: int
    borrow_date: str
    return_date: str

class BorrowCreate(BorrowBase):
    pass

class BorrowSchema(BorrowBase):
    id:int

    class Config:
        orm_mode=True





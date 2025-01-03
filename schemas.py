from pydantic import BaseModel

# Модель книги для входных и выходных данных
class BookBase(BaseModel):
    title: str
    author: str
    description: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True

class ReaderCreate(BaseModel):
    name: str
    phone: int
    address: str

class ReaderCreate(BaseModel):
    pass

class Reader(BaseModel):
    id: int

    class Config:
        orm_mode = True
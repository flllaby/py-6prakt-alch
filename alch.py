import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, MetaData, Table, Column, Integer, String, func
from datetime import datetime
from sqlalchemy.orm import session,sessionmaker
from sqlalchemy.orm import relationship
engine = create_engine(
    'sqlite:///library.db', echo=True
)

Base = declarative_base()

#------------------------------------------------------------------------------------------------------------------------------------------------    
class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    birth_year = Column(Integer)
    books = relationship('Book', back_populates='author')
#------------------------------------------------------------------------------------------------------------------------------------------------    
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    year = Column (Integer)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author', back_populates='books')
#------------------------------------------------------------------------------------------------------------------------------------------------
Session = sessionmaker(bind=engine)
session = Session()

auth1 = Author(name='Пушкин', birth_year = 1837)
auth2 = Author(name='есенин', birth_year = 1914)
auth3 = Author(name='толстый', birth_year = 1828)

book1 = Book(title='Книга есенина', year=1967, author = auth2)
book2 = Book(title='Книга толстого', year=1942, author = auth3)
book3 = Book(title='Книга толстого2', year=1676, author = auth3)
book4 = Book(title='Книга есенина2', year=1422, author = auth2)
book5 = Book(title='Книга пушкина', year=1111, author = auth1)

session.add_all([auth1, auth2, auth3, book1, book2, book3, book4, book5])
session.commit()

#------------------------------------------------------------------------------------------------------------------------------------------------
print("-----------------------------------------------------------------")
authors = session.query(Author).all()
for a in authors:
    print(a.name)
print("-----------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------------------------
authors = session.query(Author).get(1)
authors.name = "поэт какойто"
session.commit()
authors = session.query(Author).all()
for a in authors:
    print("-----------------------------------------------------------------")
    print(a.name)
    print("-----------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------------------------
book = session.query(Book).get(4)
session.delete(book)
session.commit()
books_all = session.query(Book).all()
for b in books_all:
    print("-----------------------------------------------------------------")
    print(b.title)
    print("-----------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------------------------
b = session.query(Book).order_by(Book.year.desc()).all()
for a in b:
    print("-----------------------------------------------------------------")
    print(a.title, a.year)
    print("-----------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------------------------
b = session.query(Book).filter(Book.year > 1950).all()
for a in b:
    print("-----------------------------------------------------------------")
    print(a.title, a.year)
    print("-----------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------------------------
avt = session.query(Author).filter(Author.name=='толстый').first()
if avt:
    print("-----------------------------------------------------------------")
    print(avt.name, avt.birth_year)
    print("-----------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------------------------
funct = session.query(func.count(Book.id)).scalar()
print("-----------------------------------------------------------------")
print(funct)
print("-----------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------------------------
por = session.query(Book).order_by(Book.title).limit(3).all()
for b in por:
    print("-----------------------------------------------------------------")
    print(b.title, b.year)
    print("-----------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------------------------
session.close()

Base.metadata.drop_all(engine)  
Base.metadata.create_all(engine)

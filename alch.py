from sqlite3 import connect

from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy import insert, select
from sqlalchemy import update, delete

engine = create_engine('sqlite:///library.db', echo=True)

conn = engine.connect()

metadata = MetaData()

Author = Table('authors', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(200), nullable=False),
              Column('birth_day', Integer, nullable=False))

Book = Table('books', metadata,
                Column('id', Integer, primary_key=True),
                Column('title', String, nullable=False),
                Column('year', Integer, nullable=False),
                Column('author_id', Integer, nullable=False))

metadata.create_all(engine)

ins = Author.insert().values([
    {'name': 'Пушкин', 'birth_day': 1799},
    {'name': 'Гоголь', 'birth_day': 1809},
    {'name': 'Лермонтов', 'birth_day': 1814}
])

ins = Book.insert().values([
    {'title': 'Евгений Онегин', 'year': 1833, 'author_id': 1},
    {'title': 'Мертвые души', 'year': 1842, 'author_id': 2},
    {'title': 'Герой нашего времени', 'year': 1840, 'author_id': 3},
    {'title': 'Капитанская дочка', 'year': 1836, 'author_id': 1},
    {'title': 'Ревизор', 'year': 1836, 'author_id': 2}
])

s = Author.select()
result = conn.execute(s)
for row in result:
    print(row)

upd = Author.update().where(
    Author.c.name == 'Пушкин'
).values(name='Александр Пушкин')
result = conn.execute(upd)
print(result.rowcount)

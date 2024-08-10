from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, joinedload

# SQLAlchemy Base class
Base = declarative_base()

# Author model
class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    books = relationship("Book", back_populates="author")

# Book model
class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    author = relationship("Author", back_populates="books")

# Database connection setup
DATABASE_TYPE = 'mysql'
DBAPI = 'pymysql'
HOST = 'localhost'
USER = 'root'  # Replace with your MySQL username
PASSWORD = '*******'  # Replace with your MySQL password
DATABASE = 'complexqueriesdb'

CONNECTION_STRING = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
engine = create_engine(CONNECTION_STRING)

# Create tables
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
session = Session()

def get_session():
    return session

# Insert example data
def insert_data():
    session = get_session()
    author = Author(name='George Orwell')
    book1 = Book(title='1984', author=author)
    book2 = Book(title='Animal Farm', author=author)
    
    session.add(author)
    session.add(book1)
    session.add(book2)
    session.commit()

def joined_load_example():
    session = get_session()
    books = session.query(Book).options(joinedload(Book.author)).all()
    for book in books:
        print(f"Book: {book.title}, Author: {book.author.name}")

if __name__ == "__main__":
    insert_data()
    joined_load_example()

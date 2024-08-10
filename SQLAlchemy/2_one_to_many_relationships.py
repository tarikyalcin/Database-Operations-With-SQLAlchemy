from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# SQLAlchemy Base class
Base = declarative_base()

# Author model
class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    books = relationship("Book", back_populates="author")

# Book model
class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship("Author", back_populates="books")

# Database connection setup
DATABASE_TYPE = 'mysql'
DBAPI = 'pymysql'
HOST = 'localhost'
USER = 'root'  # Replace with your MySQL username
PASSWORD = '*******'  # Replace with your MySQL password
DATABASE = 'newdatabase2'

CONNECTION_STRING = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
engine = create_engine(CONNECTION_STRING)

# Create tables
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
session = Session()

def get_session():
    return session

def create_author_and_books(author_name, book_titles):
    session = get_session()
    new_author = Author(name=author_name)
    session.add(new_author)

    for title in book_titles:
        new_book = Book(title=title, author=new_author)
        session.add(new_book)
    
    session.commit()
    print(f"New books added: {author_name}, {book_titles}")

def read_authors_and_books():
    session = get_session()
    authors = session.query(Author).all()
    for author in authors:
        print(f"Author: {author.name}")
        for book in author.books:
            print(f"Book: {book.title}")

if __name__ == "__main__":
    create_author_and_books("George Orwell", ["1984", "Animal Farm"])
    read_authors_and_books()

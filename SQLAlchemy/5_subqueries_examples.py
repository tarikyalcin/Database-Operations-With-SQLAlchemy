from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

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
DATABASE = 'subquerydb'

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
    author1 = Author(name='George Orwell')
    author2 = Author(name='Aldous Huxley')
    
    book1 = Book(title='1984', author=author1)
    book2 = Book(title='Animal Farm', author=author1)
    book3 = Book(title='Brave New World', author=author2)
    
    session.add_all([author1, author2, book1, book2, book3])
    session.commit()

# Subquery example: Count books per author
def subquery_example():
    session = get_session()
    
    # Subquery to count books for each author
    subq = session.query(
        Book.author_id,
        func.count(Book.id).label('book_count')
    ).group_by(Book.author_id).subquery()
    
    # Main query to join subquery with Author
    results = session.query(
        Author.name,
        subq.c.book_count
    ).join(subq, Author.id == subq.c.author_id).all()
    
    for name, count in results:
        print(f"Author: {name}, Book Count: {count}")

if __name__ == "__main__":
    insert_data()
    subquery_example()

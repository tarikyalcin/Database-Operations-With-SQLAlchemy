from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy Base class
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)

# Database connection setup
DATABASE_TYPE = 'mysql'
DBAPI = 'pymysql'
HOST = 'localhost'
USER = 'root'  # Replace with your MySQL username
PASSWORD = '*******'  # Replace with your MySQL password
DATABASE = 'mydatabase'

CONNECTION_STRING = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
engine = create_engine(CONNECTION_STRING)

# Create tables
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
session = Session()

def get_session():
    return session

# CRUD(Create,read,update,delete) Operations

def create_user(name, age):
    session = get_session()
    new_user = User(name=name, age=age)
    session.add(new_user)
    session.commit()
    print("New user added!")

def read_users():
    session = get_session()
    users = session.query(User).all()
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Age: {user.age}")

def update_user(name, new_age):
    session = get_session()
    user_to_update = session.query(User).filter_by(name=name).first()
    if user_to_update:
        user_to_update.age = new_age
        session.commit()
        print("User updated!")
    else:
        print("User not found!")

def delete_user(name):
    session = get_session()
    user_to_delete = session.query(User).filter_by(name=name).first()
    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
        print("User deleted!")
    else:
        print("User not found!")

if __name__ == "__main__":
    create_user("Alice", 30)
    read_users()
    update_user("Alice", 35)
    read_users()
    delete_user("Alice")

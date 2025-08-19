from sqlmodel import Field, SQLModel, create_engine, Session
import re

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)
    password: str

    def __init__(self, first_name, last_name, email, username, password):
        if not self.validate_email(email):
            raise ValueError("Invalid email format.")
        if not self.validate_password(password):
            raise ValueError("Password must be at least 8 characters long and contain letters and numbers.")
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password

    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password(password):
        return len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isalpha() for char in password)

# ایجاد پایگاه داده SQLite
DATABASE_URL = "sqlite:///users.db"
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

# ایجاد یک سشن
def get_session():
    return Session(engine)

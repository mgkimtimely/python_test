from sqlalchemy import create_engine

# SQLite 데이터베이스 연결
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)
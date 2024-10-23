from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, as_declarative

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, UUID, MetaData
from datetime import datetime, timezone
import uuid

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:superuberpass@localhost:5432/TodoApplicationDatabase'

# Check if we're using SQLite
is_sqlite = create_engine("sqlite:///").dialect.name == "sqlite"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


metadata = MetaData()

@as_declarative(metadata=metadata)
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # Default fields for all tables inheriting this class
    if is_sqlite:
        pkid = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Changed to Integer
    else:
        print('************** POSTGRES - pkid **************')
        pkid = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    if is_sqlite:
       id = Column(String, default=lambda: str(uuid.uuid4()), unique=True, index=True, nullable=False)
    else:
        print('************** POSTGRES - uuid **************')
        id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, Index=True, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
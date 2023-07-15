from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlite_file_name = "database.sqlite"
base_dir = Path(__file__).parents[1]
database_url = f"sqlite:///{base_dir / sqlite_file_name}"
engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)
Base = declarative_base()

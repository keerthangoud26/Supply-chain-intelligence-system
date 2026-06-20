from sqlalchemy import create_engine

# PostgreSQL connection
DB_URL = "postgresql://admin:admin123@localhost:5432/supplychain"

engine = create_engine(DB_URL)


def get_engine():
    return engine
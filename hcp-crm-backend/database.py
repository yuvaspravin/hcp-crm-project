from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# --- POSTGRESQL CONNECTION STRING ---
# Format: postgresql://username:password@host:port/database_name

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/hcp_crm"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- DEFINE THE DATABASE TABLE ---
class InteractionLog(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(255), index=True)
    date = Column(String(50))
    sentiment = Column(String(50))
    topics = Column(Text)
    materials = Column(Text)
    follow_ups = Column(Text)

# This command tells SQLAlchemy to look at DBeaver and create the table if it doesn't exist
Base.metadata.create_all(bind=engine)
print("SUCCESS: Python connected to Postgres and checked the tables!")
from sqlalchemy import Column, INTEGER, VARCHAR, FLOAT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Name(Base):
    __tablename__ = 'name'
    IDName = Column(INTEGER, autoincrement=True, primary_key=True)
    Year = Column(INTEGER)
    Name = Column(VARCHAR)
    Sex = Column(VARCHAR)
    Percent = Column(FLOAT)

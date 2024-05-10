from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class JobPosting(Base):
    __tablename__ = "job_postings"
    id = Column(Integer, primary_key=True, index=True)
    job_slug = Column(String, index=True, nullable=False)
    job_title = Column(String, index=True, nullable=False)
    company_name = Column(String, index=True, nullable=False)
    job_geo = Column(String, index=True, nullable=False)
    job_level = Column(String, index=True, nullable=False)
    pub_date = Column(DateTime, index=True, nullable=False)
    annual_salary = Column(Float, nullable=True)
    salary_currency = Column(String, index=True, nullable=True)
    responsibilities_1 = Column(String, index=True, nullable=False)
    responsibilities_2 = Column(String, index=True, nullable=False)
    responsibilities_3 = Column(String, index=True, nullable=False)
    file_json = Column(String, index=True)

    def save_to_db(self, db: Session):
        """
        Guarda el objeto JobPosting en la base de datos.

        :param db: Sesión de la base de datos (dependencia inyectada).
        """
        db.add(self)
        db.commit()
        db.refresh(self)

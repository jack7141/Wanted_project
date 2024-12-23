from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlmodel import Field

from app.models.base_model import BaseModel

class Company(BaseModel):
    __tablename__ = "companies"

    company_name_ko = Column(String, nullable=False)
    company_name_en = Column(String, nullable=True)
    company_name_ja = Column(String, nullable=True)

    tags = relationship("Tag", secondary="company_tags", back_populates="companies")
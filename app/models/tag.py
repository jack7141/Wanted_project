from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel
from app.models.company_tag import CompanyTag


class Tag(BaseModel):
    __tablename__ = "tags"

    tag_name_ko = Column(String, nullable=False)
    tag_name_en = Column(String, nullable=True)
    tag_name_ja = Column(String, nullable=True)

    companies = relationship("Company", secondary=CompanyTag.__table__, back_populates="tags")

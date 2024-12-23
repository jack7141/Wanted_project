from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel

class Tag(BaseModel):
    __tablename__ = "tags"

    tag_name_ko = Column(String, nullable=False)
    tag_name_en = Column(String, nullable=True)
    tag_name_ja = Column(String, nullable=True)

    companies = relationship("Company", secondary="company_tags", back_populates="tags")

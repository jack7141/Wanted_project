from sqlalchemy import Column, String, Integer, ForeignKey

from app.models.base_model import BaseModel

class CompanyTag(BaseModel):
    __tablename__ = "company_tags"

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)

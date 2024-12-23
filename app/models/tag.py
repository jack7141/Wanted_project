from sqlalchemy import Column, String
from sqlmodel import Field

from app.models.base_model import BaseModel


class Tag(BaseModel):
    user_id = Column(String, comment="상담 신청자 유저 아이디")
    course_id = Column(String, comment="코스 아이디")

import csv

from sqlalchemy.orm import Session

from app.models import Base
from app.models.company import Company
from app.models.company_tag import CompanyTag
from app.models.tag import Tag


def insert_data_from_csv(session: Session, csv_file: str):
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            company = Company(
                company_name_ko=row["company_ko"],
                company_name_en=row["company_en"] if row["company_en"] else None,
                company_name_ja=row["company_ja"] if row["company_ja"] else None,
            )
            session.add(company)
            session.commit()

            # Process tags for all languages
            tags_ko = row["tag_ko"].split("|") if row["tag_ko"] else []
            tags_en = row["tag_en"].split("|") if row["tag_en"] else []
            tags_ja = row["tag_ja"].split("|") if row["tag_ja"] else []

            for tag_ko, tag_en, tag_ja in zip(tags_ko, tags_en, tags_ja):
                tag = session.query(Tag).filter_by(
                    tag_name_ko=tag_ko, tag_name_en=tag_en, tag_name_ja=tag_ja
                ).first()
                if not tag:
                    tag = Tag(
                        tag_name_ko=tag_ko,
                        tag_name_en=tag_en,
                        tag_name_ja=tag_ja,
                    )
                    session.add(tag)
                    session.commit()

                # Create association
                company_tag = CompanyTag(company_id=company.id, tag_id=tag.id)
                session.add(company_tag)
                session.commit()

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    DATABASE_URI = "postgresql+psycopg2://postgres:password@localhost:5432/dev-wanted"
    engine = create_engine(DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Insert data from CSV
    session = SessionLocal()
    try:
        insert_data_from_csv(session, "company_tag_sample.csv")
    finally:
        session.close()
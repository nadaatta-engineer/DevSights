from sqlalchemy import Boolean, Column, Integer, String, Text

from app.database import Base


class Analysis(Base):

    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)

    build_id = Column(String, nullable=False)

    commit_id = Column(String, nullable=False)

    author = Column(String, nullable=False)

    commit_message = Column(Text, nullable=False)

    suspected_line = Column(Text, nullable=False)

    reason = Column(Text, nullable=False)

    solution = Column(Text, nullable=False)

    is_code_fix = Column(Boolean, nullable=False)

    recommended_code = Column(Text, nullable=True)
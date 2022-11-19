from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Org(Base):
    __tablename__ = "orgs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    client_name = Column(String, index=True, nullable=False)
    bills = relationship("Bill", back_populates="org")


class Bill(Base):
    __tablename__ = "bills"
    __table_args__ = (
        UniqueConstraint('org_id', 'number', name='uix_bills_org_id_number'),
    )

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("orgs.id"), nullable=False)
    org = relationship("Org", back_populates="bills")
    number = Column(Integer, nullable=False)
    sum = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    services = Column(String, nullable=False)

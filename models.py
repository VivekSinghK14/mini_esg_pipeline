from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from database import Base  


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    reporting_year = Column(Integer, nullable=False)
    scope1_value = Column(Float, nullable=False)
    scope1_unit = Column(String, nullable=False)
    scope1_tco2e = Column(Float, nullable=False)
    scope2_value = Column(Float, nullable=False)
    scope2_unit = Column(String, nullable=False)
    scope2_tco2e = Column(Float, nullable=False)
    scope3_value = Column(Float, nullable=True)
    scope3_unit = Column(String, nullable=True)
    energy_consumption_kwh = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, nullable=False)
    variant_type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    guardrail_result = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    model_name = Column(String, default="stub")
    prompt_version = Column(String, default="v1")
    duration_ms = Column(Integer, default=0)

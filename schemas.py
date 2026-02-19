from pydantic import BaseModel
from typing import Optional, Literal, List

class ReportInput(BaseModel):
    company_name: str
    reporting_year: int
    scope1_value: float
    scope1_unit: Literal["kg_co2e", "t_co2e"]
    scope2_value: float
    scope2_unit: Literal["kg_co2e", "t_co2e"]
    scope3_value: Optional[float] = None
    scope3_unit: Optional[Literal["kg_co2e", "t_co2e"]] = None
    energy_consumption_kwh: Optional[float] = None
    notes: Optional[str] = None

class StrategyVariant(BaseModel):
    variant_type: Literal["short", "neutral", "detailed"]
    content: str
    guardrail_result: Literal["pass", "warn", "fail"]

class StrategyOutput(BaseModel):
    report_id: int
    created_at: str
    duration_ms: int
    model_name: str
    prompt_version: str
    variants: List[StrategyVariant]

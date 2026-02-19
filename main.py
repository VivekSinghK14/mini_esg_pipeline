from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import time

import models
import schemas
import database




app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def normalize_to_tonnes(value: float, unit: str) -> float:
    return value / 1000 if unit == "kg_co2e" else value

@app.post("/reports")
def create_report(report: schemas.ReportInput, db: Session = Depends(get_db)):
    scope1_t = normalize_to_tonnes(report.scope1_value, report.scope1_unit)
    scope2_t = normalize_to_tonnes(report.scope2_value, report.scope2_unit)

    new_report = models.Report(
        company_name=report.company_name,
        reporting_year=report.reporting_year,
        scope1_value=report.scope1_value,
        scope1_unit=report.scope1_unit,
        scope1_tco2e=scope1_t,
        scope2_value=report.scope2_value,
        scope2_unit=report.scope2_unit,
        scope2_tco2e=scope2_t,
        scope3_value=report.scope3_value,
        scope3_unit=report.scope3_unit,
        energy_consumption_kwh=report.energy_consumption_kwh,
        notes=report.notes,
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return {"id": new_report.id, "message": "Report saved"}

@app.get("/reports/latest")
def get_latest_report(db: Session = Depends(get_db)):
    report = db.query(models.Report).order_by(models.Report.created_at.desc()).first()
    if not report:
        raise HTTPException(status_code=404, detail="No reports found")
    return report

@app.post("/reports/{id}/generate-strategy")
def generate_strategy(id: int, db: Session = Depends(get_db)):
    report = db.query(models.Report).filter(models.Report.id == id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    start = time.time()
    s1, s2, year = report.scope1_tco2e, report.scope2_tco2e, report.reporting_year

    variants = [
        ("short", f"In {year}, Scope 1 emissions were {s1} tCO2e and Scope 2 were {s2} tCO2e. Reduction efforts are planned."),
        ("neutral", f"In {year}, Scope 1 emissions totaled {s1} tCO2e and Scope 2 reached {s2} tCO2e. The company will pursue efficiency, renewable energy, and monitoring."),
        ("detailed", f"Strategy for {year}:\n- Scope 1 ({s1} tCO2e) reduction via operations.\n- Scope 2 ({s2} tCO2e) reduction via renewable energy.\n- Annual monitoring and disclosure.")
    ]

    results = []
    for vtype, content in variants:
        strategy = models.Strategy(
            report_id=id,
            variant_type=vtype,
            content=content,
            guardrail_result="pass",
            duration_ms=int((time.time() - start) * 1000),
        )
        db.add(strategy)
        db.commit()
        db.refresh(strategy)
        results.append(strategy)

    return {"report_id": id, "variants": [{"variant_type": s.variant_type, "content": s.content, "guardrail_result": s.guardrail_result} for s in results]}

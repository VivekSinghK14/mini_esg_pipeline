import requests

cases = [
    {
        "company_name": "GreenTech",
        "reporting_year": 2024,
        "scope1_value": 5000,
        "scope1_unit": "kg_co2e",
        "scope2_value": 2,
        "scope2_unit": "t_co2e"
    },
    {
        "company_name": "EcoCorp",
        "reporting_year": 2025,
        "scope1_value": 10,
        "scope1_unit": "t_co2e",
        "scope2_value": 20000,
        "scope2_unit": "kg_co2e"
    }
]

for case in cases:
    r = requests.post("http://127.0.0.1:8000/reports", json=case)
    report_id = r.json()["id"]
    s = requests.post(f"http://127.0.0.1:8000/reports/{report_id}/generate-strategy")
    data = s.json()
    print(f"Report {report_id}: {len(data['variants'])} variants generated")
    for v in data["variants"]:
        print(f" - {v['variant_type']}: {v['guardrail_result']}")

"""
GigSure Backend API Server
FastAPI backend for unified income tracking, tax estimation, and day-wise micro-insurance.
The Corporate Glitch '26 National Hackathon.
"""

import os
import io
import csv
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, UploadFile, File, Form, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.data_store import db
from backend.tax_calculator import calculate_gig_tax
from backend.ocr_engine import process_screenshot
from backend.voice_parser import parse_voice_utterance
from backend.pdf_generator import generate_income_proof_pdf

app = FastAPI(
    title="GigSure API",
    description="Financial Toolkit for Gig Workers: Unified Income, Tax Estimation, Day-Wise Micro-Insurance",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions for stats
def compute_dashboard_stats():
    records = db.get_records()
    worker = db.get_worker()
    today_str = datetime.now().strftime("%Y-%m-%d")

    today_income = 0.0
    today_expense = 0.0
    total_income = 0.0
    total_expense = 0.0
    platform_breakdown = {}
    expense_breakdown = {}

    for r in records:
        amt = float(r.get("amount", 0.0))
        rtype = r.get("type", "income")
        rdate = r.get("date", "")

        if rtype == "income":
            total_income += amt
            plat = r.get("platform", "Other")
            platform_breakdown[plat] = platform_breakdown.get(plat, 0.0) + amt
            if rdate == today_str:
                today_income += amt
        elif rtype == "expense":
            total_expense += amt
            cat = r.get("category", "Other")
            expense_breakdown[cat] = expense_breakdown.get(cat, 0.0) + amt
            if rdate == today_str:
                today_expense += amt

    net_income = total_income - total_expense
    monthly_avg_net = round(net_income / 2.0, 2) # approx 60 days of data in store

    # Safety Net Score: (Liquid savings / Daily living burn rate)
    # Target 30 days = 100 score
    liquid_savings = worker.get("liquid_savings", 21500.0)
    daily_burn = worker.get("daily_living_burn_rate", 620.0)
    runway_days = round(liquid_savings / max(1.0, daily_burn), 1)
    safety_score = min(100, int((runway_days / 30.0) * 100))

    # Social Security 90-day progress
    days_worked = worker.get("days_worked_count", 76)
    target_rule = worker.get("target_benefit_rule", 90)
    progress_pct = min(100, int((days_worked / float(target_rule)) * 100))

    return {
        "today_income": today_income,
        "today_expense": today_expense,
        "today_net": today_income - today_expense,
        "total_gross": total_income,
        "total_expenses": total_expense,
        "net_income": net_income,
        "monthly_avg_net": monthly_avg_net,
        "platform_breakdown": platform_breakdown,
        "expense_breakdown": expense_breakdown,
        "safety_score": safety_score,
        "runway_days": runway_days,
        "days_worked": days_worked,
        "target_rule": target_rule,
        "rule_progress_pct": progress_pct
    }

@app.get("/api/profile")
def get_profile():
    return db.get_worker()

@app.get("/api/dashboard")
def get_dashboard():
    stats = compute_dashboard_stats()
    worker = db.get_worker()
    insurance = db.get_insurance()
    recent = sorted(db.get_records(), key=lambda x: x.get("date", ""), reverse=True)[:15]
    return {
        "worker": worker,
        "stats": stats,
        "insurance": insurance,
        "recent_records": recent
    }

class LogEntry(BaseModel):
    type: str # income or expense
    platform: Optional[str] = None
    category: Optional[str] = None
    amount: float
    trips: Optional[int] = None
    description: Optional[str] = None
    date: Optional[str] = None

@app.post("/api/transactions/log")
def log_transaction(entry: LogEntry):
    data = entry.dict()
    if not data.get("date"):
        data["date"] = datetime.now().strftime("%Y-%m-%d")
    record = db.add_record(data)
    return {"status": "success", "record": record}

@app.post("/api/transactions/ocr")
async def ocr_upload(file: UploadFile = File(...)):
    contents = await file.read()
    ocr_result = process_screenshot(contents)
    
    # Auto-add as an income record if confirmed
    record = {
        "type": "income",
        "platform": ocr_result.get("platform", "Gig Platform"),
        "amount": ocr_result.get("gross_payout", 4500.0),
        "trips": ocr_result.get("trips_count", 50),
        "description": f"Verified OCR payout ({ocr_result.get('payout_period', 'Weekly')})",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "metadata": {
            "incentives": ocr_result.get("incentives", 0.0),
            "deductions": ocr_result.get("deductions", 0.0),
            "raw_text": ocr_result.get("raw_text_detected", [])
        }
    }
    saved_record = db.add_record(record)
    
    return {
        "status": "success",
        "ocr_result": ocr_result,
        "saved_record": saved_record
    }

class VoiceUtterance(BaseModel):
    text: str

@app.post("/api/transactions/voice")
def parse_voice(body: VoiceUtterance):
    parsed = parse_voice_utterance(body.text)
    saved_items = []
    
    # Save parsed income items
    for inc in parsed.get("incomes", []):
        r = db.add_record({
            "type": "income",
            "platform": inc.get("platform", "Swiggy"),
            "amount": inc.get("amount", 0.0),
            "description": inc.get("description", "Voice logged income")
        })
        saved_items.append(r)
        
    # Save parsed expense items
    for exp in parsed.get("expenses", []):
        r = db.add_record({
            "type": "expense",
            "category": exp.get("category", "Fuel"),
            "amount": exp.get("amount", 0.0),
            "description": exp.get("description", "Voice logged expense")
        })
        saved_items.append(r)

    return {
        "status": "success",
        "parsed": parsed,
        "saved_items": saved_items
    }

@app.post("/api/transactions/csv-upload")
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    reader = csv.DictReader(io.StringIO(text))
    
    count = 0
    for row in reader:
        try:
            amt = float(row.get("amount", 0.0))
            if amt <= 0:
                continue
            rec_type = row.get("type", "income").strip().lower()
            record = {
                "date": row.get("date", datetime.now().strftime("%Y-%m-%d")),
                "type": rec_type,
                "amount": amt,
                "platform": row.get("platform", "Swiggy") if rec_type == "income" else None,
                "category": row.get("category", "Fuel") if rec_type == "expense" else None,
                "trips": int(row.get("trips", 0)) if row.get("trips") else None,
                "description": row.get("description", "CSV imported entry")
            }
            db.add_record(record)
            count += 1
        except Exception:
            continue
            
    return {"status": "success", "records_imported": count}

@app.get("/api/transactions/sample-csv")
def download_sample_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["date", "type", "platform", "category", "amount", "trips", "description"])
    writer.writerow(["2026-11-10", "income", "Swiggy", "", "980.00", "12", "Dinner peak deliveries"])
    writer.writerow(["2026-11-10", "expense", "", "Fuel", "220.00", "", "Petrol 2L"])
    writer.writerow(["2026-11-11", "income", "Uber", "", "1450.00", "9", "Airport and city rides"])
    writer.writerow(["2026-11-11", "expense", "", "Fuel", "310.00", "", "CNG top up"])
    writer.writerow(["2026-11-12", "income", "Zomato", "", "840.00", "10", "Lunch rush orders"])
    writer.writerow(["2026-11-12", "expense", "", "Maintenance", "150.00", "", "Puncture & chain lube"])
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=gigsure_sample_earnings.csv"}
    )

@app.get("/api/tax/estimate")
def get_tax_estimate():
    stats = compute_dashboard_stats()
    # Annualized gross estimate
    annualized_gross = stats["total_gross"] * 4.0 # 60 days * 6 ~ 360 days
    tax_result = calculate_gig_tax(
        annual_gross_income=annualized_gross,
        documented_expenses=stats["total_expenses"] * 4.0
    )
    return {
        "stats": stats,
        "tax_calculation": tax_result
    }

@app.get("/api/insurance/status")
def get_insurance_status():
    ins = db.get_insurance()
    worker = db.get_worker()
    return {
        "insurance": ins,
        "days_worked_count": worker.get("days_worked_count", 76),
        "target_benefit_rule": worker.get("target_benefit_rule", 90)
    }

class InsuranceToggle(BaseModel):
    active: bool

@app.post("/api/insurance/toggle")
def toggle_day_insurance(body: InsuranceToggle):
    updated = db.toggle_insurance(body.active)
    return {
        "status": "success",
        "message": f"Day-wise accident cover {'ACTIVATED' if body.active else 'DEACTIVATED'}",
        "insurance": updated
    }

class ClaimRequest(BaseModel):
    type: str
    description: str
    estimated_amount: float

@app.post("/api/insurance/claim")
def submit_claim(body: ClaimRequest):
    import uuid
    claim_id = f"CLM-2026-{uuid.uuid4().hex[:5].upper()}"
    claim = {
        "claim_id": claim_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "type": body.type,
        "description": body.description,
        "claimed": body.estimated_amount,
        "settled": 0.0,
        "status": "Under Review · Cashless Hospitalization Assured within 2 hrs"
    }
    db.data["insurance"]["claims_history"].insert(0, claim)
    db._save()
    return {"status": "success", "claim": claim}

@app.get("/api/schemes")
def get_matched_schemes():
    return [
        {
            "id": "e_shram",
            "name": "e-Shram Central Social Security Portal",
            "provider": "Ministry of Labour & Employment",
            "description": "National database of unorganized & gig workers providing Universal Account Number (UAN) and priority welfare benefits.",
            "eligibility": "Gig & Platform workers aged 16-59",
            "cost": "Free (100% Govt Funded)",
            "benefits": "₹2,00,000 accidental cover, pension fund linkage, portability across states.",
            "status": "Registered & Active (UAN-8834-9102-7712)"
        },
        {
            "id": "pmsby",
            "name": "Pradhan Mantri Suraksha Bima Yojana (PMSBY)",
            "provider": "Govt of India / Bank Auto-Debit",
            "description": "Ultra-low-cost micro accident insurance for accidental death or permanent disability.",
            "eligibility": "Savings bank account holder aged 18-70",
            "cost": "₹20 / Year (₹1.60 / month)",
            "benefits": "₹2,00,000 for accidental death / total disability, ₹1,00,000 for partial disability.",
            "status": "Eligible · 1-Click Link with Bank Account"
        },
        {
            "id": "pmjjby",
            "name": "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)",
            "provider": "Life Insurance Corporation / Banks",
            "description": "Renewable term life insurance cover for gig worker families.",
            "eligibility": "Aged 18-50 with bank account",
            "cost": "₹436 / Year (₹36 / month)",
            "benefits": "₹2,00,000 life risk cover payable to nominee on demise from any cause.",
            "status": "Eligible · Recommended"
        },
        {
            "id": "state_gig_welfare",
            "name": "Social Security Code 2026 - State Gig Welfare Fund",
            "provider": "Karnataka / Rajasthan Gig Workers Welfare Board",
            "description": "Statutory social security fund financed by 1-2% platform fee levy on each transaction.",
            "eligibility": "Minimum 90 days logged across platforms in a calendar year",
            "cost": "Zero Cost to Worker (Funded by Aggregator Cess)",
            "benefits": "Health insurance, maternity benefits, children scholarship, occupational disease grant.",
            "status": "76 / 90 Days Completed (14 Days Remaining)"
        }
    ]

@app.get("/api/forecasting")
def get_forecast():
    # Heatmap of best hours and 7-day projection
    hours = [
        {"hour": "06:00 - 09:00", "label": "Morning Commute", "avg_rate": "₹110/hr", "demand": "Moderate", "platforms": ["Uber Moto", "Rapido", "Blinkit"]},
        {"hour": "09:00 - 12:00", "label": "Office Morning Rush", "avg_rate": "₹145/hr", "demand": "High", "platforms": ["Uber Auto", "Ola", "Zepto"]},
        {"hour": "12:00 - 15:30", "label": "Lunch Food Peak", "avg_rate": "₹185/hr", "demand": "Very High", "platforms": ["Swiggy", "Zomato"]},
        {"hour": "15:30 - 18:30", "label": "Afternoon Grocery Lull", "avg_rate": "₹95/hr", "demand": "Low", "platforms": ["Blinkit", "Zepto", "Porter"]},
        {"hour": "18:30 - 23:00", "label": "Evening Rush & Dinner", "avg_rate": "₹230/hr", "demand": "Peak Surge", "platforms": ["Swiggy", "Zomato", "Uber Auto"]},
        {"hour": "23:00 - 02:00", "label": "Late Night Munchies", "avg_rate": "₹170/hr", "demand": "High", "platforms": ["Swiggy Instamart", "Zomato"]}
    ]
    
    today = datetime.now()
    seven_day_forecast = []
    base = 1100
    for i in range(1, 8):
        fday = today + timedelta(days=i)
        mult = 1.35 if fday.weekday() in [4, 5, 6] else 0.95
        pred_earning = round(base * mult)
        seven_day_forecast.append({
            "day": fday.strftime("%a (%d %b)"),
            "predicted_earnings": pred_earning,
            "fuel_forecast": round(pred_earning * 0.22),
            "net_forecast": round(pred_earning * 0.78),
            "is_weekend": fday.weekday() in [4, 5, 6]
        })
        
    return {
        "best_hours": hours,
        "seven_day_forecast": seven_day_forecast,
        "recommendation": "Shift 2 hours from 3:30 PM lull to 8:30-10:30 PM dinner surge to boost weekly net take-home by ~₹1,850."
    }

@app.get("/api/reports/income-proof-pdf")
def get_pdf():
    worker = db.get_worker()
    stats = compute_dashboard_stats()
    annualized_gross = stats["total_gross"] * 4.0
    tax_info = calculate_gig_tax(annualized_gross, stats["total_expenses"] * 4.0)
    pdf_bytes = generate_income_proof_pdf(worker, stats, tax_info)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=GigSure_Income_Proof_{worker.get('name', 'Worker').replace(' ', '_')}.pdf"}
    )

@app.post("/api/trust/reset-data")
def reset_user_data():
    db.reset_data()
    return {"status": "success", "message": "All financial records and consent tokens have been reset."}

# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "GigSure backend is operational."}

"""
GigSure In-Memory & File Persisted Financial Data Store
Stores worker transactions, profile, insurance state, and forecasting metrics.
"""

import json
import os
from datetime import datetime, timedelta
import random

DATA_FILE = os.path.join(os.path.dirname(__file__), "gig_data.json")

def generate_default_data():
    today = datetime.now()
    records = []
    platforms = ["Swiggy", "Uber", "Zomato", "Zepto"]
    
    # Generate 60 days of realistic past records
    cumulative_days = 0
    for i in range(60, 0, -1):
        dt = today - timedelta(days=i)
        date_str = dt.strftime("%Y-%m-%d")
        
        # Gig workers typically work 5 to 6 days a week
        if dt.weekday() == 1 and i % 3 == 0:
            continue # rest day
            
        cumulative_days += 1
        
        # Primary platform for the day
        p1 = "Swiggy" if i % 2 == 0 else "Uber"
        amt1 = random.randint(650, 1150)
        trips1 = random.randint(8, 14)
        
        records.append({
            "id": f"tx-inc-{date_str}-1",
            "date": date_str,
            "type": "income",
            "platform": p1,
            "amount": amt1,
            "trips": trips1,
            "description": f"{p1} delivery/rides payout"
        })
        
        # Occasional secondary platform surge
        if i % 3 == 0:
            p2 = "Zepto" if p1 == "Swiggy" else "Zomato"
            amt2 = random.randint(350, 650)
            trips2 = random.randint(4, 7)
            records.append({
                "id": f"tx-inc-{date_str}-2",
                "date": date_str,
                "type": "income",
                "platform": p2,
                "amount": amt2,
                "trips": trips2,
                "description": f"{p2} peak surge earnings"
            })
            
        # Fuel expense for the day
        fuel_amt = random.randint(180, 290)
        records.append({
            "id": f"tx-exp-{date_str}-fuel",
            "date": date_str,
            "type": "expense",
            "category": "Fuel",
            "amount": fuel_amt,
            "description": "Daily bike petrol"
        })
        
        # Monthly bike EMI on 5th of month
        if dt.day == 5:
            records.append({
                "id": f"tx-exp-{date_str}-emi",
                "date": date_str,
                "type": "expense",
                "category": "EMI",
                "amount": 2850.0,
                "description": "Hero Splendor bike loan EMI"
            })

    # Today's records
    today_str = today.strftime("%Y-%m-%d")
    cumulative_days += 1
    records.append({
        "id": f"tx-inc-{today_str}-1",
        "date": today_str,
        "type": "income",
        "platform": "Swiggy",
        "amount": 890.0,
        "trips": 11,
        "description": "Lunch + evening food deliveries"
    })
    records.append({
        "id": f"tx-exp-{today_str}-fuel",
        "date": today_str,
        "type": "expense",
        "category": "Fuel",
        "amount": 220.0,
        "description": "Morning petrol top-up (2.1 Liters)"
    })

    return {
        "worker": {
            "name": "Rajesh Kumar",
            "phone": "+91 98765 43210",
            "city": "Bengaluru, Karnataka",
            "vehicle": "Hero Splendor Plus (Two-Wheeler)",
            "vehicle_number": "KA 05 EQ 8421",
            "primary_platforms": ["Swiggy", "Uber", "Zepto"],
            "e_shram_uan": "UAN-8834-9102-7712",
            "e_shram_registered": True,
            "bank_account_verified": True,
            "liquid_savings": 21500.0,
            "daily_living_burn_rate": 620.0,
            "days_worked_count": 76,  # toward 90/120 day benefit rule
            "target_benefit_rule": 90
        },
        "insurance": {
            "active_today": True,
            "policy_id": "GS-DIGIT-2026-99241",
            "provider": "Digit Micro-Sure (Mock IRDAI Licensed Partner)",
            "activated_at": f"{today_str}T08:30:00",
            "expires_at": f"{today_str}T23:59:59",
            "daily_cost": 5.0,
            "coverages": {
                "accidental_death_disability": 200000.0,
                "road_hospitalization": 50000.0,
                "loss_of_income_daily": 500.0
            },
            "claims_history": [
                {
                    "claim_id": "CLM-2026-031",
                    "date": "2026-09-14",
                    "type": "Emergency Outpatient Treatment (Minor Skid)",
                    "claimed": 3800.0,
                    "settled": 3800.0,
                    "status": "Settled in 4 hrs"
                }
            ]
        },
        "records": records
    }

class DataStore:
    def __init__(self):
        self.data = self._load()

    def _load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        data = generate_default_data()
        self._save(data)
        return data

    def _save(self, data=None):
        if data is None:
            data = self.data
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")

    def get_worker(self):
        return self.data["worker"]

    def update_worker(self, updates):
        self.data["worker"].update(updates)
        self._save()
        return self.data["worker"]

    def get_records(self):
        return self.data["records"]

    def add_record(self, record):
        if "id" not in record:
            record["id"] = f"tx-{len(self.data['records'])+1}-{int(datetime.now().timestamp())}"
        if "date" not in record:
            record["date"] = datetime.now().strftime("%Y-%m-%d")
        self.data["records"].append(record)
        self._save()
        return record

    def get_insurance(self):
        return self.data["insurance"]

    def toggle_insurance(self, state: bool):
        today_str = datetime.now().strftime("%Y-%m-%d")
        self.data["insurance"]["active_today"] = state
        if state:
            import uuid
            self.data["insurance"]["policy_id"] = f"GS-DIGIT-2026-{uuid.uuid4().hex[:6].upper()}"
            self.data["insurance"]["activated_at"] = datetime.now().isoformat()
            self.data["insurance"]["expires_at"] = f"{today_str}T23:59:59"
            # Deduct ₹5 daily micro-premium as expense
            self.add_record({
                "date": today_str,
                "type": "expense",
                "category": "Micro-Insurance",
                "amount": 5.0,
                "description": f"Day-wise accident cover policy {self.data['insurance']['policy_id']}"
            })
            # Increment days worked count if not counted today
            self.data["worker"]["days_worked_count"] = min(120, self.data["worker"]["days_worked_count"] + 1)
        self._save()
        return self.data["insurance"]

    def reset_data(self):
        self.data = generate_default_data()
        self._save()
        return self.data

db = DataStore()

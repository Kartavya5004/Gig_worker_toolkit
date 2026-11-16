"""
Generates high-fidelity mock payout screenshot images for Swiggy, Zomato, and Uber
so that judges and users can test RapidOCR with 1 click.
"""

import os
from PIL import Image, ImageDraw, ImageFont

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "samples")
os.makedirs(SAMPLE_DIR, exist_ok=True)

def create_swiggy_screenshot():
    img = Image.new("RGB", (600, 850), color="#F4F5F7")
    d = ImageDraw.Draw(img)

    # Header
    d.rectangle([(0, 0), (600, 110)], fill="#FC8019") # Swiggy Orange
    d.text((30, 30), "SWIGGY DELIVERY PARTNER", fill="#FFFFFF")
    d.text((30, 65), "Weekly Payout Statement · 08 Nov - 14 Nov 2026", fill="#FFFFFF")

    # Main Card
    d.rectangle([(30, 140), (570, 300)], fill="#FFFFFF", outline="#E2E8F0", width=2)
    d.text((50, 160), "Total Payout Transferred to Bank", fill="#64748B")
    d.text((50, 195), "Rs 5,420.00", fill="#0F172A")
    d.text((50, 255), "Status: Deposited on 15 Nov | HDFC Bank **8421", fill="#16A34A")

    # Order Breakdown
    d.rectangle([(30, 320), (570, 540)], fill="#FFFFFF", outline="#E2E8F0", width=2)
    d.text((50, 340), "EARNINGS BREAKDOWN", fill="#0F172A")
    d.line([(50, 370), (550, 370)], fill="#E2E8F0", width=1)
    
    items = [
        ("Base Order Pay (68 Deliveries)", "Rs 3,850.00"),
        ("Customer Tips (14 tips)", "Rs 420.00"),
        ("Peak Dinner Target Incentive", "Rs 1,150.00"),
        ("TDS Deduction (Sec 194-O, 1%)", "- Rs 54.20"),
        ("Bag / Uniform EMI Deduction", "- Rs 125.80"),
    ]
    y = 390
    for label, val in items:
        d.text((50, y), label, fill="#334155")
        d.text((430, y), val, fill="#0F172A")
        y += 28

    # Performance
    d.rectangle([(30, 560), (570, 680)], fill="#FFFFFF", outline="#E2E8F0", width=2)
    d.text((50, 580), "WEEKLY METRICS", fill="#0F172A")
    d.text((50, 615), "Total Distance Traveled: 312 km", fill="#64748B")
    d.text((50, 640), "Customer Rating: 4.92 ★ (Super Partner)", fill="#F59E0B")

    # Footer
    d.text((150, 780), "Swiggy Fleet Finance & Tax Division", fill="#94A3B8")

    out_path = os.path.join(SAMPLE_DIR, "swiggy_payout.png")
    img.save(out_path)
    return out_path

def create_zomato_screenshot():
    img = Image.new("RGB", (600, 850), color="#1E2024")
    d = ImageDraw.Draw(img)

    # Header
    d.rectangle([(0, 0), (600, 110)], fill="#E23744") # Zomato Red
    d.text((30, 30), "ZOMATO DELIVERY FLEET", fill="#FFFFFF")
    d.text((30, 65), "Weekly Statement · Period: 01 Nov - 07 Nov 2026", fill="#FFFFFF")

    # Main Card
    d.rectangle([(30, 140), (570, 300)], fill="#272A30", outline="#3E424B", width=2)
    d.text((50, 160), "Net Weekly Earnings Credited", fill="#9CA3AF")
    d.text((50, 195), "Rs 4,890.00", fill="#FFFFFF")
    d.text((50, 255), "Direct UPI Transfer Completed: OKICICI", fill="#22C55E")

    # Breakdown
    d.rectangle([(30, 320), (570, 540)], fill="#272A30", outline="#3E424B", width=2)
    d.text((50, 340), "SUMMARY STATEMENT", fill="#FFFFFF")
    d.line([(50, 370), (550, 370)], fill="#3E424B", width=1)

    items = [
        ("Completed Orders (54 Orders)", "Rs 3,240.00"),
        ("Weekend Target Incentive Bonus", "Rs 1,200.00"),
        ("Rain Surge Surcharge", "Rs 450.00"),
        ("Platform Regulatory Deduction", "- Rs 48.90"),
        ("Order Adjustments", "Rs 0.00"),
    ]
    y = 390
    for label, val in items:
        d.text((50, y), label, fill="#D1D5DB")
        d.text((430, y), val, fill="#FFFFFF")
        y += 28

    # Footer stats
    d.rectangle([(30, 560), (570, 680)], fill="#272A30", outline="#3E424B", width=2)
    d.text((50, 580), "Zomato Diamond Partner Badge Active", fill="#FBBF24")
    d.text((50, 615), "Login Hours Logged: 38.5 hrs", fill="#9CA3AF")
    d.text((50, 640), "Acceptance Rate: 96%", fill="#9CA3AF")

    out_path = os.path.join(SAMPLE_DIR, "zomato_payout.png")
    img.save(out_path)
    return out_path

def create_uber_screenshot():
    img = Image.new("RGB", (600, 850), color="#F8FAFC")
    d = ImageDraw.Draw(img)

    # Header
    d.rectangle([(0, 0), (600, 110)], fill="#000000") # Uber Black
    d.text((30, 30), "UBER DRIVER PARTNER", fill="#FFFFFF")
    d.text((30, 65), "Weekly Statement · 02 Nov - 08 Nov 2026", fill="#FFFFFF")

    # Main Card
    d.rectangle([(30, 140), (570, 300)], fill="#FFFFFF", outline="#E2E8F0", width=2)
    d.text((50, 160), "Your Total Weekly Balance", fill="#64748B")
    d.text((50, 195), "Rs 8,150.00", fill="#000000")
    d.text((50, 255), "Processed via NEFT to SBI Account", fill="#16A34A")

    # Breakdown
    d.rectangle([(30, 320), (570, 540)], fill="#FFFFFF", outline="#E2E8F0", width=2)
    d.text((50, 340), "TRIP EARNINGS DETAILS", fill="#0F172A")
    d.line([(50, 370), (550, 370)], fill="#E2E8F0", width=1)

    items = [
        ("Gross Fares (45 Trips)", "Rs 9,480.00"),
        ("Airport Toll Reimbursements", "Rs 320.00"),
        ("Quest Bonus Tier 2", "Rs 800.00"),
        ("Uber Service Fee (Commission)", "- Rs 2,370.00"),
        ("TDS Section 194-O (1%)", "- Rs 80.00"),
    ]
    y = 390
    for label, val in items:
        d.text((50, y), label, fill="#334155")
        d.text((430, y), val, fill="#0F172A")
        y += 28

    # Footer
    d.rectangle([(30, 560), (570, 680)], fill="#FFFFFF", outline="#E2E8F0", width=2)
    d.text((50, 580), "DRIVER RATING: 4.88 ★", fill="#0F172A")
    d.text((50, 615), "Total Online Hours: 42.0 hrs", fill="#64748B")
    d.text((50, 640), "Compliments Received: Clean Auto, Great Music", fill="#64748B")

    out_path = os.path.join(SAMPLE_DIR, "uber_payout.png")
    img.save(out_path)
    return out_path

if __name__ == "__main__":
    f1 = create_swiggy_screenshot()
    f2 = create_zomato_screenshot()
    f3 = create_uber_screenshot()
    print("Generated mock screenshots:", f1, f2, f3)

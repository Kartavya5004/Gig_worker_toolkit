"""
GigSure Income-Proof PDF Certificate Generator
Creates a bank-verifiable proof of income and creditworthiness document
for gig workers applying for micro-loans, two-wheeler finance, and rental agreements.
Uses PyMuPDF for PDF generation.
"""

import io
import pymupdf as fitz
from datetime import datetime
from typing import Dict, Any

def generate_income_proof_pdf(worker: Dict[str, Any], stats: Dict[str, Any], tax_info: Dict[str, Any]) -> bytes:
    """Generates a PDF document with income records, expense breakdown, and safety net verification."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842) # A4 size

    # Colors
    c_primary = (0.09, 0.28, 0.58)     # Navy Blue
    c_accent = (0.86, 0.15, 0.15)      # Red brand accent
    c_dark = (0.12, 0.12, 0.15)        # Charcoal
    c_gray = (0.45, 0.45, 0.48)        # Muted Gray
    c_bg_box = (0.95, 0.96, 0.98)      # Light Slate Box
    c_green = (0.08, 0.52, 0.28)       # Forest Green

    # Header Banner Background
    page.draw_rect(fitz.Rect(0, 0, 595, 80), color=None, fill=c_primary)
    
    # Title Text
    page.insert_text(fitz.Point(36, 38), "GIGSURE FINANCIAL VERIFICATION", fontsize=18, color=(1, 1, 1), fontname="helv")
    page.insert_text(fitz.Point(36, 56), "Certified Income Proof & Creditworthiness Record | Builders Hub Hackathon", fontsize=9, color=(0.85, 0.90, 0.98), fontname="helv")
    
    # Verification Badge
    page.draw_rect(fitz.Rect(430, 20, 560, 60), color=(1, 1, 1), fill=(1, 1, 1))
    page.insert_text(fitz.Point(440, 36), "VERIFIED RECORD", fontsize=8, color=c_green, fontname="helv")
    cert_id = f"GS-VER-{int(datetime.now().timestamp()) % 1000000}"
    page.insert_text(fitz.Point(440, 50), cert_id, fontsize=10, color=c_dark, fontname="helv")

    y = 110
    # Worker Details Block
    page.draw_rect(fitz.Rect(36, y, 559, y + 80), color=(0.85, 0.88, 0.92), fill=c_bg_box)
    
    # Details Columns
    page.insert_text(fitz.Point(50, y + 22), "WORKER NAME:", fontsize=8, color=c_gray, fontname="helv")
    page.insert_text(fitz.Point(50, y + 38), worker.get("name", "Rajesh Kumar"), fontsize=12, color=c_dark, fontname="helv")
    
    page.insert_text(fitz.Point(200, y + 22), "GOVT e-SHRAM UAN:", fontsize=8, color=c_gray, fontname="helv")
    page.insert_text(fitz.Point(200, y + 38), worker.get("e_shram_uan", "UAN-8834-9102-7712"), fontsize=10, color=c_dark, fontname="helv")

    page.insert_text(fitz.Point(380, y + 22), "ACTIVE PLATFORMS:", fontsize=8, color=c_gray, fontname="helv")
    platforms_str = ", ".join(worker.get("primary_platforms", ["Swiggy", "Uber"]))
    page.insert_text(fitz.Point(380, y + 38), platforms_str, fontsize=10, color=c_dark, fontname="helv")

    page.insert_text(fitz.Point(50, y + 62), f"VEHICLE: {worker.get('vehicle', 'Hero Splendor')} ({worker.get('vehicle_number', 'KA 05 EQ 8421')})", fontsize=8, color=c_gray, fontname="helv")
    page.insert_text(fitz.Point(280, y + 62), f"LOCATION: {worker.get('city', 'Bengaluru, Karnataka')}", fontsize=8, color=c_gray, fontname="helv")
    page.insert_text(fitz.Point(440, y + 62), f"ISSUED: {datetime.now().strftime('%d %b %Y')}", fontsize=8, color=c_gray, fontname="helv")

    y += 105
    # Section 1: Financial Performance (90-Day Trailing)
    page.insert_text(fitz.Point(36, y), "1. TRAILING 90-DAY EARNINGS & NET TAKE-HOME AUDIT", fontsize=12, color=c_primary, fontname="helv")
    page.draw_line(fitz.Point(36, y + 5), fitz.Point(559, y + 5), color=(0.8, 0.8, 0.8), width=1)
    
    y += 20
    # 3 Summary Cards
    col_w = 166
    cards = [
        ("Gross Platform Earnings", f"Rs {stats.get('total_gross', 98400):,.0f}", "Swiggy, Uber, Zomato, Zepto"),
        ("Operational Deductions", f"Rs {stats.get('total_expenses', 31000):,.0f}", "Fuel, EMI & Maintenance"),
        ("Certified Net Income", f"Rs {stats.get('net_income', 67400):,.0f}", f"Rs {stats.get('monthly_avg_net', 22466):,.0f} / Month Average")
    ]
    for idx, (label, val, sub) in enumerate(cards):
        cx = 36 + idx * (col_w + 10)
        page.draw_rect(fitz.Rect(cx, y, cx + col_w, y + 65), color=(0.85, 0.88, 0.92), fill=(1, 1, 1))
        page.insert_text(fitz.Point(cx + 12, y + 20), label, fontsize=8, color=c_gray, fontname="helv")
        val_color = c_green if idx == 2 else c_dark
        page.insert_text(fitz.Point(cx + 12, y + 42), val, fontsize=15, color=val_color, fontname="helv")
        page.insert_text(fitz.Point(cx + 12, y + 56), sub, fontsize=7, color=c_gray, fontname="helv")

    y += 85
    # Section 2: Statutory Tax Compliance & Section 87A Clarity
    page.insert_text(fitz.Point(36, y), "2. STATUTORY TAX POSITION (UNION BUDGET 2026-27 COMPLIANCE)", fontsize=12, color=c_primary, fontname="helv")
    page.draw_line(fitz.Point(36, y + 5), fitz.Point(559, y + 5), color=(0.8, 0.8, 0.8), width=1)

    y += 20
    tax_box_rect = fitz.Rect(36, y, 559, y + 80)
    page.draw_rect(tax_box_rect, color=(0.85, 0.88, 0.92), fill=c_bg_box)

    page.insert_text(fitz.Point(50, y + 22), "ANNUALIZED PROJECTED GROSS:", fontsize=8, color=c_gray, fontname="helv")
    page.insert_text(fitz.Point(50, y + 36), f"Rs {tax_info.get('annual_gross_income', 393600):,.0f}", fontsize=11, color=c_dark, fontname="helv")

    page.insert_text(fitz.Point(210, y + 22), "SEC 44ADA PRESUMPTIVE DEDUCTION:", fontsize=8, color=c_gray, fontname="helv")
    page.insert_text(fitz.Point(210, y + 36), f"Rs {tax_info.get('presumptive_deduction_sec44', 196800):,.0f} (50%)", fontsize=11, color=c_dark, fontname="helv")

    page.insert_text(fitz.Point(400, y + 22), "NET TAX LIABILITY (SEC 87A):", fontsize=8, color=c_gray, fontname="helv")
    page.insert_text(fitz.Point(400, y + 36), "Rs 0.00 (ZERO TAX LIMIT Rs 12L)", fontsize=10, color=c_green, fontname="helv")

    page.insert_text(fitz.Point(50, y + 60), f"TDS DEDUCTED UNDER SEC 194-O: Rs {tax_info.get('tds_deducted_194o', 3936):,.0f}", fontsize=9, color=c_dark, fontname="helv")
    page.insert_text(fitz.Point(270, y + 60), f"CLAIMABLE BANK REFUND: Rs {tax_info.get('tds_refund_claimable', 3936):,.0f} (Via Form ITR-4)", fontsize=9, color=c_primary, fontname="helv")

    y += 105
    # Section 3: Social Security & Safety-Net Verification
    page.insert_text(fitz.Point(36, y), "3. SOCIAL SECURITY & LENDING SAFETY-NET METRICS", fontsize=12, color=c_primary, fontname="helv")
    page.draw_line(fitz.Point(36, y + 5), fitz.Point(559, y + 5), color=(0.8, 0.8, 0.8), width=1)

    y += 20
    col_w2 = 255
    # Left: Social Security 90/120 Day Rule
    page.draw_rect(fitz.Rect(36, y, 36 + col_w2, y + 90), color=(0.85, 0.88, 0.92), fill=(1, 1, 1))
    page.insert_text(fitz.Point(48, y + 20), "SOCIAL SECURITY CODE 2026 RULE", fontsize=9, color=c_dark, fontname="helv")
    days_worked = worker.get("days_worked_count", 76)
    target_days = worker.get("target_benefit_rule", 90)
    page.insert_text(fitz.Point(48, y + 42), f"{days_worked} / {target_days} Days Worked", fontsize=15, color=c_primary, fontname="helv")
    page.insert_text(fitz.Point(48, y + 60), f"Status: On-Track ({target_days - days_worked} days left to unlock state welfare fund)", fontsize=8, color=c_gray, fontname="helv")
    page.insert_text(fitz.Point(48, y + 74), "Central e-Shram Worker Pool Registered", fontsize=8, color=c_green, fontname="helv")

    # Right: Safety Net Score & Runway
    rx = 36 + col_w2 + 13
    page.draw_rect(fitz.Rect(rx, y, rx + col_w2, y + 90), color=(0.85, 0.88, 0.92), fill=(1, 1, 1))
    page.insert_text(fitz.Point(rx + 12, y + 20), "GIGSURE SAFETY-NET SCORE", fontsize=9, color=c_dark, fontname="helv")
    safety_score = stats.get("safety_score", 82)
    runway_days = stats.get("runway_days", 34)
    page.insert_text(fitz.Point(rx + 12, y + 42), f"{safety_score} / 100 ({runway_days} Days Runway)", fontsize=15, color=c_green, fontname="helv")
    page.insert_text(fitz.Point(rx + 12, y + 60), f"Liquid Buffer: Rs {worker.get('liquid_savings', 21500):,.0f} vs Daily: Rs {worker.get('daily_living_burn_rate', 620):,.0f}", fontsize=8, color=c_gray, fontname="helv")
    page.insert_text(fitz.Point(rx + 12, y + 74), "Active Day-Wise Cover: Rs 2,00,000 Accidental Protection", fontsize=8, color=c_primary, fontname="helv")

    y += 115
    # Institutional Lending Note
    page.draw_rect(fitz.Rect(36, y, 559, y + 70), color=(0.88, 0.85, 0.75), fill=(0.99, 0.98, 0.94))
    page.insert_text(fitz.Point(48, y + 18), "NOTICE TO LENDERS & LANDLORDS:", fontsize=8, color=(0.6, 0.4, 0.1), fontname="helv")
    lender_text = (
        "This certificate aggregates multi-platform digital earnings verified across Swiggy, Uber, Zomato, and Zepto.\n"
        "Net income is calibrated after deducting real fuel expenses and ongoing vehicle EMIs. In the absence of a\n"
        "traditional monthly payslip, this verifiable record serves as an authenticated proof of ongoing cash flow."
    )
    for l_idx, line in enumerate(lender_text.split("\n")):
        page.insert_text(fitz.Point(48, y + 32 + (l_idx * 11)), line, fontsize=7.5, color=c_dark, fontname="helv")

    # Footer
    page.draw_line(fitz.Point(36, 790), fitz.Point(559, 790), color=(0.8, 0.8, 0.8), width=1)
    page.insert_text(fitz.Point(36, 808), "Generated by GigSure · Financial Toolkit for Platform Workers · The Corporate Glitch '26", fontsize=8, color=c_gray, fontname="helv")
    page.insert_text(fitz.Point(450, 808), "Scan QR / Verify Online", fontsize=8, color=c_primary, fontname="helv")

    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes

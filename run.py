"""
GigSure Startup Script
Runs the unified FastAPI server & web application on http://localhost:8000
"""

import sys
import os

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("[*] GIGSURE - Financial Toolkit for Gig Workers")
    print("    The Corporate Glitch '26 National Hackathon")
    print("=" * 60)
    print("Starting server on http://localhost:8000")
    print("Features:")
    print(" - Unified Income Tracker (Swiggy, Uber, Zomato, Zepto)")
    print(" - Real-time RapidOCR Payout Screenshot Scanner")
    print(" - Web Speech Voice Entry (Hindi / English)")
    print(" - FY 2026-27 New Tax Regime Engine & Sec 194-O TDS Refund")
    print(" - Bank-Ready Certified Income Proof PDF Generator")
    print(" - Day-Wise Micro-Insurance Switch (Rs 5/day accident cover)")
    print(" - Social Security Code 2026 90-Day Tracker")
    print("=" * 60)
    
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)

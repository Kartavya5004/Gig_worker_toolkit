# GigSure 🛡️
### A Financial Toolkit for Gig Workers: Unified Income Tracking, Tax Estimation, and Day-Wise Micro-Insurance
**National Level Hackathon — The Corporate Glitch '26 | Builders Hub**

---

## 📌 Problem Context
- India has over **12+ million gig and platform workers** (projected to reach 23.5M by 2030).
- **4 in 10** earn under ₹15,000/month.
- **62.2%** lack health insurance, and **44.2%** lack accident insurance.
- **Zero payslips**: Banks and landlords reject gig workers for loans and rentals because platform earnings are fragmented across Swiggy, Uber, Zomato, and Zepto with no proof of income.
- **Tax confusion**: Workers do not know that under the FY 2026-27 Union Budget New Tax Regime, earnings under ₹12 Lakh owe **₹0 tax**, nor that they can claim back their **1% TDS** deducted by platforms under Section 194-O.
- **Policy gap**: Under the Social Security Code 2026, workers who complete 90 or 120 days on aggregator platforms qualify for state welfare benefits, yet only ~1 in 10 is registered and tracked on e-Shram.

---

## 💡 Solution: The 5-Pillar Architecture

```
[1. INPUT]                  [2. PROCESS]               [3. RULES]                   [4. OUTPUT]                [5. PROTECT]
CSV, Voice (Hindi/Eng),  -> Clean & categorize,     -> Tax estimate (Sec 87A),   -> Dashboard, tax set-aside -> Partner Insurer API
Payout Screenshot OCR       Compute True Net Take-     90/120-day rule count,       Income-Proof PDF,          Day-wise accident cover
                            Home, AI peak hours        e-Shram scheme match         Safety-Net Score           switched ON / OFF
```

### 1. 📊 Unified Income & "True Net" Tracker
- Consolidates earnings across **Swiggy, Uber, Zomato, and Zepto**.
- Calibrates **gross payouts vs real operational deductions** (Fuel ~25-35%, vehicle EMI, and maintenance) to reveal the worker's **True Net Take-Home**.
- **AI Peak Hours Optimizer**: Recommends the highest-paying windows (e.g. Lunch surge ₹185/hr vs Dinner surge ₹230/hr) to maximize hourly yield.

### 2. 🎙️ Voice-First & Screenshot OCR Ingestion
- **RapidOCR ONNX Engine**: Instant OCR scanning of weekly payout statements from Swiggy, Zomato, and Uber. Extracts base pay, order count, peak surge bonuses, and TDS deductions with 95%+ confidence.
- **Voice Ingestion (Web Speech API)**: Speak naturally in Hindi, Hinglish, or English (e.g., *"आज स्विगी से 850 कमाए और 200 का पेट्रोल भरा"*). Automatically extracts income and expense line items with audio Text-To-Speech feedback.
- **1-Click Test Presets**: Test real payout statement images with a single click.

### 3. 📑 Certified Income-Proof PDF Generator (Banker & Landlord Ready)
- Produces an official, verifiable **"GigSure Certified Income & Credit Stability Certificate"** via `PyMuPDF`.
- Features 60-day multi-platform income records, verified net operating cashflow, digital QR verification, e-Shram UAN badge, and vehicle compliance.
- Provides gig workers with an authentic alternative to traditional salary slips for two-wheeler financing and apartment leases.

### 4. 🛡️ Day-Wise Micro-Insurance Switch (The Core USP!)
- Gig workers work irregularly; rigid annual insurance is unaffordable.
- **The 1-Tap Switch**: Workers toggle cover **only on the days they ride** for **₹5/day**.
- Issues instant policy ID (`GS-DIGIT-2026-XXXX`) under simulated IRDAI partner sandbox:
  - **₹2,00,000** Accidental Death / Permanent Disability
  - **₹50,000** Emergency Road Hospitalization
  - **₹500/day** Loss of Income Allowance
- Emergency SOS button with 1-click cashless claim dispatch.

### 5. 🎯 Social Security 90-Day Tracker & Safety-Net Score
- **90/120-Day Benefit Rule**: Tracks cumulative active days toward the Social Security Code 2026 threshold to unlock State Gig Worker Welfare Fund benefits.
- **Safety-Net Score**: Evaluates emergency runway (Liquid Savings ÷ Daily Living Burn Rate).
- **Automated Scheme Matcher**: 1-click guide for e-Shram registration, PMSBY (₹20/year accident cover), PMJJBY (life cover), and Ayushman Bharat PM-JAY.

---

## 🛠️ Tech Stack
| Component | Technology | Purpose |
|---|---|---|
| **Frontend** | Responsive PWA (HTML5, Tailwind CSS, Lucide Icons, Chart.js) | Mobile-first UI with Bilingual English/Hindi toggle & Mobile Shell view |
| **Backend** | Python FastAPI & Uvicorn | High-performance async API with strict validation |
| **OCR** | RapidOCR ONNX Runtime & Pillow | Local, low-latency OCR for platform payout screenshots |
| **Voice & Audio** | Web Speech API & SpeechSynthesis | Hands-free Hindi/Hinglish voice entry for low-literacy workers |
| **Reports** | PyMuPDF (fitz) | Bank-verifiable certified Income-Proof PDF generation |
| **Data Engine** | In-memory & JSON Persistence | Local encryption & complete worker data sovereignty (Right to Erasure) |

---

## 🚀 Running the Prototype

### 1. Launch the Server
From the project root directory, run:
```bash
python run.py
```

The unified FastAPI server will start on:
👉 **`http://localhost:8000`**

### 2. Live Interactive Features to Test:
1. **Interactive Dashboard**: View real-time gross vs fuel deductions, 60-day trailing ledger, and platform distribution chart.
2. **Day-Wise Micro-Insurance Switch**: Toggle the emerald switch at the top right to simulate policy issuance (`GS-DIGIT-2026-XXXX`) and ₹5 deduction.
3. **Screenshot OCR Scanner**: Head to the "OCR & Voice Log" tab and click any 1-click sample statement (*Swiggy, Zomato, Uber*) or upload your own screenshot.
4. **Voice Entry**: Click the microphone icon or tap a sample Hindi prompt (*"आज स्विगी से 850 कमाए और 200 का पेट्रोल भरा"*). Listen to the voice feedback!
5. **Download Certified Income-Proof PDF**: Go to the "Tax & Loan Proof" tab and click **"Download Certified PDF"** to get the loan certificate.
6. **Bilingual Toggle**: Click the language button in the header to switch between **English** and **हिंदी (Hindi)**.
7. **Mobile Frame Toggle**: Click the "Mobile View" button in the header to see how the application renders on delivery riders' smartphones!

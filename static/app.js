/**
 * GigSure - Front-End Application Logic
 * Supports Voice Entry (Web Speech API), RapidOCR screenshot ingestion,
 * Tax calculation, Day-Wise Micro-Insurance toggle, and English/Hindi localization.
 */

// Global State
let appState = {
  lang: 'en', // 'en' or 'hi'
  isMobileView: false,
  insuranceActive: true,
  worker: {},
  stats: {},
  insurance: {},
  records: [],
  bestHours: [],
  schemes: [],
  lastVoiceSummary: ""
};

// Bilingual Translations Dictionary
const I18N = {
  en: {
    appTagline: "Financial Safety & Income Toolkit",
    tab_dashboard: "Dashboard & Net",
    tab_ingest: "OCR & Voice Log",
    tab_tax: "Tax & Loan Proof",
    tab_protect: "Protect & 90-Days",
    tab_trust: "Trust & Privacy",
    card_gross: "Today's Gross Payouts",
    card_fuel: "Fuel & Operating Cost",
    card_net: "True Net Take-Home",
    net_margin_label: "74.7% Net Realization",
    history_headline: "60-Day Multi-Platform Income Record",
    btn_gen_loan_pdf: "View Loan-Ready Certificate",
    title_platform_dist: "Earnings By Platform",
    title_best_hours: "AI Peak Hours Optimizer",
    best_hours_desc: "Earning rates based on real-time order surges and trip fares:",
    title_recent_tx: "Recent Inflow & Deductions",
    ingest_header: "Voice-First & Screenshot Ingestion Layer",
    ingest_subtitle: "No tedious manual typing. Read payouts from screenshots, speak in Hindi/English, or import CSV.",
    title_voice_log: "Voice Entry (Web Speech API)",
    voice_desc: "Tap the microphone and speak naturally (e.g. 'आज स्विगी से 850 कमाए और 200 का पेट्रोल भरा'):",
    tap_to_speak: "Tap to record voice entry",
    lbl_one_tap_demo: "Or tap sample voice prompt:",
    title_ocr_payout: "Payout Screenshot OCR",
    ocr_desc: "Upload your weekly statement screenshot from Swiggy, Zomato, Uber, or Ola. Our engine extracts payouts, incentives, and deductions:",
    upload_prompt: "Click or drag screenshot here",
    lbl_one_tap_ocr: "1-Click Test with Realistic Statements:",
    title_manual_log: "Quick Manual Entry",
    title_csv_import: "CSV Bulk Import",
    csv_desc: "Import statements from Excel or bank aggregation files in one click:",
    tax_banner_title: "Zero Tax Clarity & Section 194-O TDS Refund",
    tax_banner_desc: "Most gig workers earn between ₹2.5L and ₹4.5L annually. Under the New Tax Regime (rebate up to ₹12 Lakh), your tax is ₹0. Better yet, you can claim your 1% TDS back!",
    btn_download_official_pdf: "Download Certified PDF",
    title_tds_refund: "Section 194-O TDS Refund Eligibility",
    subtitle_tds_refund: "Platform aggregators automatically deduct 1% TDS on your total payouts.",
    btn_claim_refund: "How to Claim TDS Refund",
    title_proof_doc: "Certified Income Proof Document (For Banks & Landlords)",
    btn_download_income_pdf: "Download Official PDF Certificate",
    btn_preview_cert: "Interactive Fullscreen Preview",
    protect_hero_title: "Day-Wise Micro-Accident Cover",
    protect_hero_desc: "Traditional annual insurance is too expensive. GigSure switches on cover only on the days you ride. Just ₹5 for ₹2,00,000 protection while on shift!",
    btn_emergency_sos: "Emergency Claim SOS",
    title_schemes: "Matched Government Welfare Schemes"
  },
  hi: {
    appTagline: "गिग वर्कर्स के लिए आय ट्रैकिंग, टैक्स और बीमा टूलकिट",
    tab_dashboard: "डैशबोर्ड और नेट कमाई",
    tab_ingest: "आवाज़ और OCR रसीद",
    tab_tax: "टैक्स और लोन प्रमाण",
    tab_protect: "दैनिक सुरक्षा बीमा (90 दिन)",
    tab_trust: "सुरक्षा और प्राइवेसी",
    card_gross: "आज की कुल कमाई (Gross)",
    card_fuel: "पेट्रोल और चालू खर्चे",
    card_net: "वास्तविक शुद्ध बचत (Net)",
    net_margin_label: "74.7% वास्तविक शुद्ध मार्जिन",
    history_headline: "60 दिनों का मल्टी-प्लेटफ़ॉर्म आय रिकॉर्ड",
    btn_gen_loan_pdf: "लोन सर्टिफिकेट देखें",
    title_platform_dist: "प्लेटफ़ॉर्म के अनुसार आय",
    title_best_hours: "AI पीक ऑवर सुझाव (ज्यादा कमाई)",
    best_hours_desc: "ऑर्डर सर्ज और किराए के आधार पर प्रति घंटे औसत कमाई दर:",
    title_recent_tx: "हाल के लेन-देन",
    ingest_header: "आवाज़ और स्क्रीनशॉट इनपुट",
    ingest_subtitle: "बिना टाइपिंग के सीधे स्क्रीनशॉट स्कैन करें या हिंदी में बोलकर रिकॉर्ड दर्ज करें।",
    title_voice_log: "आवाज़ से दर्ज करें (हिंदी / Hinglish)",
    voice_desc: "माइक बटन दबाएं और बोलें (जैसे: 'आज स्विगी से 850 कमाए और 200 का पेट्रोल भरा'):",
    tap_to_speak: "बोलने के लिए माइक दबाएं",
    lbl_one_tap_demo: "या इन उदाहरणों पर क्लिक करें:",
    title_ocr_payout: "स्क्रीनशॉट OCR पे-आउट स्कैनर",
    ocr_desc: "स्विगी, जोमैटो, उबर या ओला की वीकली स्टेटमेंट अपलोड करें। इंजन अपने-आप डेटा निकाल लेगा:",
    upload_prompt: "स्क्रीनशॉट यहां अपलोड करें",
    lbl_one_tap_ocr: "1-क्लिक टेस्ट (नमूना पे-आउट):",
    title_manual_log: "मैन्युअल एंट्री",
    title_csv_import: "CSV फ़ाइल इम्पोर्ट",
    csv_desc: "एक्सेल या बैंक स्टेटमेंट की CSV एक क्लिक में इम्पोर्ट करें:",
    tax_banner_title: "शून्य टैक्स ₹0 और 1% TDS रिफंड",
    tax_banner_desc: "नए बजट 2026-27 के तहत ₹12 लाख तक की आय पर कोई टैक्स नहीं है (धारा 87A)। आपका कटा हुआ 1% TDS आपको बैंक खाते में वापस मिलेगा!",
    btn_download_official_pdf: "प्रमाणित PDF डाउनलोड करें",
    title_tds_refund: "धारा 194-O TDS रिफंड पात्रता",
    subtitle_tds_refund: "स्विगी और उबर हर पे-आउट पर 1% TDS काटते हैं जिसे आप पूरा वापस पा सकते हैं।",
    btn_claim_refund: "TDS वापस पाने का तरीका",
    title_proof_doc: "लोन व किराये हेतु आय प्रमाण पत्र",
    btn_download_income_pdf: "प्रमाणित आय प्रमाण पत्र PDF",
    btn_preview_cert: "स्क्रीन पर सर्टिफिकेट देखें",
    protect_hero_title: "दिन-वार माइक्रो एक्सीडेंट कवर (₹5/दिन)",
    protect_hero_desc: "सालाना पॉलिसी महंगी होती है। GigSure केवल आपके काम वाले दिनों पर ₹5 में ₹2 लाख का एक्सीडेंट कवर सक्रिय करता है!",
    btn_emergency_sos: "आपातकालीन क्लेम SOS",
    title_schemes: "सरकारी कल्याणकारी योजनाएं"
  }
};

let platformPieChart = null;

// Initialize on Load
document.addEventListener("DOMContentLoaded", () => {
  fetchDashboardData();
  fetchForecast();
  fetchSchemes();
  lucide.createIcons();
});

// Switch Tab
function switchTab(tabName) {
  const tabs = ['dashboard', 'ingestion', 'tax', 'protect', 'trust'];
  tabs.forEach(t => {
    const view = document.getElementById(`view-${t}`);
    const btn = document.getElementById(`tab-${t}`);
    if (view && btn) {
      if (t === tabName) {
        view.classList.remove('hidden');
        btn.classList.add('active-tab');
        btn.classList.remove('text-slate-400');
        btn.classList.add('text-white');
      } else {
        view.classList.add('hidden');
        btn.classList.remove('active-tab');
        btn.classList.add('text-slate-400');
        btn.classList.remove('text-white');
      }
    }
  });
  lucide.createIcons();
}

// Toggle Language
function toggleLanguage() {
  appState.lang = appState.lang === 'en' ? 'hi' : 'en';
  const label = document.getElementById('currentLangLabel');
  if (label) {
    label.innerText = appState.lang === 'en' ? 'हिंदी' : 'English';
  }
  applyTranslations();
}

function applyTranslations() {
  const dict = I18N[appState.lang];
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      el.innerHTML = dict[key];
    }
  });
  const tag = document.getElementById('appTagline');
  if (tag) tag.innerText = dict.appTagline;
  updateInsuranceUI();
}

// Toggle Device View (Desktop full vs Mobile frame)
function toggleDeviceView() {
  const container = document.getElementById('appContainer');
  const label = document.getElementById('deviceViewLabel');
  appState.isMobileView = !appState.isMobileView;
  if (appState.isMobileView) {
    container.classList.add('mobile-frame');
    label.innerText = 'Desktop View';
  } else {
    container.classList.remove('mobile-frame');
    label.innerText = 'Mobile View';
  }
}

// Fetch Main Dashboard Data
async function fetchDashboardData() {
  try {
    const res = await fetch('/api/dashboard');
    const data = await res.json();
    appState.worker = data.worker;
    appState.stats = data.stats;
    appState.insurance = data.insurance;
    appState.records = data.recent_records;
    appState.insuranceActive = data.insurance.active_today;

    renderDashboardMetrics();
    renderTransactionsTable();
    renderPlatformChart();
    updateInsuranceUI();
    fetchTaxEstimate();
  } catch (err) {
    console.error("Error fetching dashboard:", err);
  }
}

// Render Dashboard Metrics
function renderDashboardMetrics() {
  const s = appState.stats;
  if (!s) return;

  const grossEl = document.getElementById('dashTodayGross');
  const expEl = document.getElementById('dashTodayExpense');
  const netEl = document.getElementById('dashTodayNet');
  const totGrossEl = document.getElementById('dashTotalGross');
  const totExpEl = document.getElementById('dashTotalExp');
  const totNetEl = document.getElementById('dashTotalNet');

  if (grossEl) grossEl.innerText = `₹${Math.round(s.today_income)}`;
  if (expEl) expEl.innerText = `-₹${Math.round(s.today_expense)}`;
  if (netEl) netEl.innerText = `₹${Math.round(s.today_net)}`;
  if (totGrossEl) totGrossEl.innerText = `₹${Math.round(s.total_gross).toLocaleString('en-IN')}`;
  if (totExpEl) totExpEl.innerText = `₹${Math.round(s.total_expenses).toLocaleString('en-IN')}`;
  if (totNetEl) totNetEl.innerText = `₹${Math.round(s.net_income).toLocaleString('en-IN')}`;

  // 90-Day Tracker
  const daysCount = document.getElementById('workedDaysCount');
  const progress = document.getElementById('workedDaysProgressBar');
  const daysLeft = document.getElementById('daysRemainingCount');
  if (daysCount) daysCount.innerText = s.days_worked;
  if (progress) progress.style.width = `${s.rule_progress_pct}%`;
  if (daysLeft) daysLeft.innerText = `${s.target_rule - s.days_worked} days left`;

  // Safety score
  const safetyScore = document.getElementById('safetyScoreDisplay');
  const runway = document.getElementById('runwayDaysDisplay');
  if (safetyScore) safetyScore.innerText = s.safety_score;
  if (runway) runway.innerText = `${s.runway_days} Days`;
}

// Render Transactions Ledger
function renderTransactionsTable() {
  const container = document.getElementById('recentTxTable');
  if (!container) return;

  const recs = appState.records || [];
  container.innerHTML = recs.map(r => {
    const isInc = r.type === 'income';
    const sign = isInc ? '+' : '-';
    const color = isInc ? 'text-emerald-400' : 'text-rose-400';
    const icon = isInc ? 'arrow-down-left' : 'arrow-up-right';
    const label = isInc ? (r.platform || 'Platform Pay') : (r.category || 'Cost');

    return `
      <div class="py-2.5 flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 rounded-lg ${isInc ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'} flex items-center justify-center">
            <i data-lucide="${icon}" class="w-4 h-4"></i>
          </div>
          <div>
            <div class="font-semibold text-slate-200">${label}</div>
            <div class="text-[10px] text-slate-500">${r.date} • ${r.description || ''}</div>
          </div>
        </div>
        <div class="text-right">
          <div class="font-bold ${color}">${sign}₹${Math.round(r.amount).toLocaleString('en-IN')}</div>
          ${r.trips ? `<div class="text-[10px] text-slate-500">${r.trips} trips</div>` : ''}
        </div>
      </div>
    `;
  }).join('');
  lucide.createIcons();
}

// Render Platform Distribution Chart
function renderPlatformChart() {
  const ctx = document.getElementById('platformChart');
  if (!ctx) return;

  const bd = appState.stats.platform_breakdown || { Swiggy: 45000, Uber: 32000, Zepto: 12000, Zomato: 9400 };
  const labels = Object.keys(bd);
  const data = Object.values(bd);

  if (platformPieChart) {
    platformPieChart.destroy();
  }

  platformPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: ['#FC8019', '#000000', '#7C3AED', '#E23744', '#10B981'],
        borderColor: '#1e293b',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: { color: '#cbd5e1', font: { size: 11 } }
        }
      },
      cutout: '65%'
    }
  });
}

// Fetch Forecast and Best Hours
async function fetchForecast() {
  try {
    const res = await fetch('/api/forecasting');
    const data = await res.json();
    appState.bestHours = data.best_hours;

    const list = document.getElementById('bestHoursList');
    if (list) {
      list.innerHTML = data.best_hours.map(h => {
        const isPeak = h.demand.includes('Peak') || h.demand.includes('Very');
        return `
          <div class="p-2 rounded-lg bg-slate-950 border ${isPeak ? 'border-amber-500/40 bg-amber-950/10' : 'border-slate-800'} flex items-center justify-between">
            <div>
              <span class="font-bold ${isPeak ? 'text-amber-400' : 'text-slate-300'}">${h.hour}</span>
              <span class="text-[10px] text-slate-500 ml-1.5">• ${h.label}</span>
            </div>
            <div class="flex items-center space-x-2">
              <span class="font-bold text-white">${h.avg_rate}</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded ${isPeak ? 'bg-amber-500/20 text-amber-300' : 'bg-slate-800 text-slate-400'}">${h.demand}</span>
            </div>
          </div>
        `;
      }).join('');
    }
    const recText = document.getElementById('aiRecommendationText');
    if (recText && data.recommendation) {
      recText.innerText = data.recommendation;
    }
  } catch (err) {
    console.error("Error fetching forecast:", err);
  }
}

// Fetch Matched Schemes
async function fetchSchemes() {
  try {
    const res = await fetch('/api/schemes');
    const schemes = await res.json();
    appState.schemes = schemes;

    const container = document.getElementById('schemesList');
    if (container) {
      container.innerHTML = schemes.map(s => `
        <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-1">
              <span class="font-bold text-slate-200 text-xs">${s.name}</span>
              <span class="text-[10px] px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 font-medium">${s.cost}</span>
            </div>
            <p class="text-slate-400 text-[11px] mb-2">${s.description}</p>
            <div class="text-[11px] text-emerald-400 font-medium mb-1">Benefit: ${s.benefits}</div>
          </div>
          <div class="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[10px]">
            <span class="text-slate-500">${s.status}</span>
            <span class="text-blue-400 font-semibold cursor-pointer hover:underline">Apply / View</span>
          </div>
        </div>
      `).join('');
    }
  } catch (err) {
    console.error("Error fetching schemes:", err);
  }
}

// Fetch Tax Estimate
async function fetchTaxEstimate() {
  try {
    const res = await fetch('/api/tax/estimate');
    const data = await res.json();
    const t = data.tax_calculation;

    const annGross = document.getElementById('taxAnnualGross');
    const presDed = document.getElementById('taxPresumptiveDed');
    const taxPay = document.getElementById('taxPayableAmount');
    const tdsVal = document.getElementById('tdsDeductedValue');

    if (annGross) annGross.innerText = `₹${Math.round(t.annual_gross_income).toLocaleString('en-IN')}`;
    if (presDed) presDed.innerText = `₹${Math.round(t.presumptive_deduction_sec44).toLocaleString('en-IN')}`;
    if (taxPay) taxPay.innerText = `₹${t.final_tax_payable.toFixed(2)}`;
    if (tdsVal) tdsVal.innerText = `₹${Math.round(t.tds_deducted_194o).toLocaleString('en-IN')}.00`;
  } catch (err) {
    console.error("Error fetching tax estimate:", err);
  }
}

// Day-Wise Micro Insurance Toggle
async function toggleInsurance() {
  const newState = !appState.insuranceActive;
  try {
    const res = await fetch('/api/insurance/toggle', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ active: newState })
    });
    const data = await res.json();
    appState.insuranceActive = newState;
    appState.insurance = data.insurance;
    updateInsuranceUI();
    fetchDashboardData();
  } catch (err) {
    console.error("Error toggling insurance:", err);
  }
}

function updateInsuranceUI() {
  const dot = document.getElementById('shieldStatusDot');
  const text = document.getElementById('shieldStatusText');
  const sub = document.getElementById('shieldSubtitle');
  const btn = document.getElementById('toggleInsuranceBtn');
  const ind = document.getElementById('toggleIndicator');
  const shiftBadge = document.getElementById('shiftIndicatorBadge');
  const protectPill = document.getElementById('protectStatusPill');

  const isEn = appState.lang === 'en';

  if (appState.insuranceActive) {
    if (dot) {
      dot.className = "w-2 h-2 rounded-full bg-emerald-500 animate-pulse";
    }
    if (text) {
      text.className = "text-xs font-bold text-emerald-400";
      text.innerText = isEn ? "Day-Shield: ACTIVE" : "डे-शील्ड: सक्रिय (Active)";
    }
    if (sub) {
      sub.innerText = isEn ? "₹2,00,000 cover · ₹5/day" : "₹2 लाख बीमा · ₹5/दिन";
    }
    if (btn) btn.className = "relative inline-flex h-7 w-13 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent bg-emerald-600 transition-colors duration-200 ease-in-out focus:outline-none";
    if (ind) ind.className = "translate-x-6 inline-block h-6 w-6 transform rounded-full bg-white shadow-md transition duration-200 ease-in-out";
    if (shiftBadge) {
      shiftBadge.innerText = isEn ? "COVERED TODAY" : "आज सुरक्षित";
      shiftBadge.className = "text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold";
    }
    if (protectPill) protectPill.innerText = `Active Policy: ${appState.insurance.policy_id || 'GS-DIGIT-2026-99241'}`;
  } else {
    if (dot) {
      dot.className = "w-2 h-2 rounded-full bg-amber-500";
    }
    if (text) {
      text.className = "text-xs font-bold text-amber-400";
      text.innerText = isEn ? "Day-Shield: OFF" : "डे-शील्ड: बंद (OFF)";
    }
    if (sub) {
      sub.innerText = isEn ? "Tap switch to protect shift" : "सुरक्षा चालू करने के लिए दबाएं";
    }
    if (btn) btn.className = "relative inline-flex h-7 w-13 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent bg-slate-700 transition-colors duration-200 ease-in-out focus:outline-none";
    if (ind) ind.className = "translate-x-0 inline-block h-6 w-6 transform rounded-full bg-slate-400 shadow-md transition duration-200 ease-in-out";
    if (shiftBadge) {
      shiftBadge.innerText = isEn ? "NOT COVERED" : "कवर नहीं";
      shiftBadge.className = "text-[10px] px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold";
    }
    if (protectPill) protectPill.innerText = isEn ? "No active policy today" : "आज कोई पॉलिसी सक्रिय नहीं";
  }
}

// ------------------- VOICE INPUT (Web Speech API) -------------------
let recognition = null;
let isRecording = false;

function toggleVoiceRecording() {
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    // If browser doesn't have Web Speech API, run demo utterance
    simulateVoice("आज स्विगी से 850 कमाए और 200 का पेट्रोल भरा");
    return;
  }

  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!recognition) {
    recognition = new SpeechRec();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = appState.lang === 'hi' ? 'hi-IN' : 'en-IN';

    recognition.onstart = () => {
      isRecording = true;
      document.getElementById('recordingStatus').innerText = "Listening... Speak now";
      document.getElementById('voiceWaveAnimation').classList.remove('hidden');
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      processVoiceTranscript(transcript);
    };

    recognition.onerror = () => {
      isRecording = false;
      document.getElementById('recordingStatus').innerText = "Tap to record voice entry";
      document.getElementById('voiceWaveAnimation').classList.add('hidden');
    };

    recognition.onend = () => {
      isRecording = false;
      document.getElementById('recordingStatus').innerText = "Tap to record voice entry";
      document.getElementById('voiceWaveAnimation').classList.add('hidden');
    };
  }

  if (!isRecording) {
    recognition.start();
  } else {
    recognition.stop();
  }
}

async function simulateVoice(text) {
  document.getElementById('recordingStatus').innerText = `Simulating: "${text}"`;
  document.getElementById('voiceWaveAnimation').classList.remove('hidden');
  setTimeout(() => {
    document.getElementById('voiceWaveAnimation').classList.add('hidden');
    document.getElementById('recordingStatus').innerText = "Tap to record voice entry";
    processVoiceTranscript(text);
  }, 1000);
}

async function processVoiceTranscript(text) {
  try {
    const res = await fetch('/api/transactions/voice', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    const p = data.parsed;

    const box = document.getElementById('voiceResultBox');
    const resultText = document.getElementById('voiceResultText');
    box.classList.remove('hidden');

    const summary = appState.lang === 'hi' ? p.summary_hindi : p.summary_english;
    appState.lastVoiceSummary = summary;
    resultText.innerText = summary;

    speakVoiceSummary();
    fetchDashboardData();
  } catch (err) {
    console.error("Error processing voice:", err);
  }
}

function speakVoiceSummary() {
  if ('speechSynthesis' in window && appState.lastVoiceSummary) {
    const utterance = new SpeechSynthesisUtterance(appState.lastVoiceSummary);
    utterance.lang = appState.lang === 'hi' ? 'hi-IN' : 'en-IN';
    window.speechSynthesis.speak(utterance);
  }
}

// ------------------- SCREENSHOT OCR -------------------
async function handleOcrFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  await uploadAndProcessScreenshot(file);
}

async function testPresetOcr(platform) {
  try {
    // Fetch pre-generated sample image
    const response = await fetch(`/static/samples/${platform}_payout.png`);
    const blob = await response.blob();
    const file = new File([blob], `${platform}_payout.png`, { type: "image/png" });
    await uploadAndProcessScreenshot(file);
  } catch (err) {
    console.error("Error running preset OCR:", err);
  }
}

async function uploadAndProcessScreenshot(file) {
  const formData = new FormData();
  formData.append("file", file);

  const box = document.getElementById('ocrResultBox');
  box.classList.remove('hidden');
  document.getElementById('ocrResultPlatform').innerText = "Scanning image with RapidOCR...";

  try {
    const res = await fetch('/api/transactions/ocr', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    const ocr = data.ocr_result;

    document.getElementById('ocrResultPlatform').innerText = `${ocr.platform} Statement Verified`;
    document.getElementById('ocrGrossAmount').innerText = `₹${Math.round(ocr.gross_payout).toLocaleString('en-IN')}`;
    document.getElementById('ocrTripCount').innerText = `${ocr.trips_count} orders`;
    document.getElementById('ocrIncentive').innerText = `₹${Math.round(ocr.incentives)}`;
    document.getElementById('ocrDeductions').innerText = `-₹${Math.round(ocr.deductions)}`;
    document.getElementById('ocrPeriodLabel').innerText = `Period: ${ocr.payout_period || 'Nov 2026'}`;

    fetchDashboardData();
  } catch (err) {
    console.error("OCR upload error:", err);
  }
}

// Manual Quick Entry
async function submitManualLog() {
  const type = document.getElementById('manType').value;
  const cat = document.getElementById('manCat').value;
  const amt = parseFloat(document.getElementById('manAmount').value);
  const desc = document.getElementById('manDesc').value;

  if (isNaN(amt) || amt <= 0) {
    alert("Please enter a valid amount.");
    return;
  }

  const payload = {
    type: type,
    amount: amt,
    description: desc || `${cat} entry`,
    platform: type === 'income' ? cat : null,
    category: type === 'expense' ? cat : null
  };

  try {
    await fetch('/api/transactions/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    document.getElementById('manAmount').value = '';
    document.getElementById('manDesc').value = '';
    fetchDashboardData();
    alert("Record successfully saved.");
  } catch (err) {
    console.error("Error logging manual entry:", err);
  }
}

// CSV Bulk Upload
async function handleCsvUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch('/api/transactions/csv-upload', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    alert(`Successfully imported ${data.records_imported} records from CSV.`);
    fetchDashboardData();
  } catch (err) {
    console.error("Error uploading CSV:", err);
  }
}

// Modals
function openEmergencyClaimModal() {
  document.getElementById('emergencyClaimModal').classList.remove('hidden');
}

function previewCertificateModal() {
  document.getElementById('certificateModal').classList.remove('hidden');
}

function showItrGuideModal() {
  document.getElementById('itrGuideModal').classList.remove('hidden');
}

function closeModal(id) {
  document.getElementById(id).classList.add('hidden');
}

async function submitEmergencyClaim() {
  const type = document.getElementById('claimTypeSelect').value;
  const amount = parseFloat(document.getElementById('claimAmountInput').value) || 3000;
  const loc = document.getElementById('claimLocationInput').value;

  try {
    const res = await fetch('/api/insurance/claim', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: type,
        description: `Emergency claim at ${loc}`,
        estimated_amount: amount
      })
    });
    const data = await res.json();
    closeModal('emergencyClaimModal');
    alert(`Instant Claim Filed: ${data.claim.claim_id}\nCashless admission authorized for ₹${amount}. Our medical desk is reaching out.`);
  } catch (err) {
    console.error("Error submitting claim:", err);
  }
}

// Trust Layer Actions
function exportAllDataJson() {
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(appState, null, 2));
  const dlAnchorElem = document.createElement('a');
  dlAnchorElem.setAttribute("href", dataStr);
  dlAnchorElem.setAttribute("download", `gigsure_data_export_${new Date().toISOString().slice(0, 10)}.json`);
  dlAnchorElem.click();
}

async function confirmResetData() {
  if (confirm("Are you sure you want to erase all your financial records and reset to default?")) {
    try {
      await fetch('/api/trust/reset-data', { method: 'POST' });
      fetchDashboardData();
      alert("All records have been reset.");
    } catch (err) {
      console.error("Reset error:", err);
    }
  }
}

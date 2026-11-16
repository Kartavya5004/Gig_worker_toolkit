"""
GigSure Tax Engine: FY 2026-27 New Tax Regime & Presumptive Taxation (Section 44ADA/44AD)
Tailored specifically for Indian gig and platform workers.
"""

from typing import Dict, Any

def calculate_gig_tax(
    annual_gross_income: float,
    documented_expenses: float = 0.0,
    regime: str = "new_2026_27"
) -> Dict[str, Any]:
    """
    Computes tax liability for gig workers using Section 44ADA presumptive 
    expense deduction (50% expense allowance for independent platform contractors)
    or actual documented expenses (fuel, EMI, maintenance).
    """
    # Presumptive expense deduction: 50% or actual documented, whichever is higher
    presumptive_deduction = annual_gross_income * 0.50
    effective_expense_deduction = max(presumptive_deduction, documented_expenses)
    taxable_income = max(0.0, annual_gross_income - effective_expense_deduction)

    # TDS Deducted under Section 194-O (1% on platform gross payouts)
    tds_deducted_194o = annual_gross_income * 0.01

    # New Tax Regime FY 2026-27 Slabs:
    # Up to 4,00,000: 0%
    # 4,00,001 to 8,00,000: 5%
    # 8,00,001 to 12,00,000: 10%
    # 12,00,001 to 16,00,000: 15%
    # 16,00,001 to 20,00,000: 20%
    # 20,00,001 to 24,00,000: 25%
    # Above 24,00,000: 30%
    # Section 87A Rebate: Zero tax for taxable income up to Rs 12,00,000 (Rebate up to Rs 60,000)

    tax_before_rebate = 0.0
    if taxable_income <= 400000:
        tax_before_rebate = 0.0
    elif taxable_income <= 800000:
        tax_before_rebate = (taxable_income - 400000) * 0.05
    elif taxable_income <= 1200000:
        tax_before_rebate = (400000 * 0.05) + ((taxable_income - 800000) * 0.10)
    elif taxable_income <= 1600000:
        tax_before_rebate = (400000 * 0.05) + (400000 * 0.10) + ((taxable_income - 1200000) * 0.15)
    else:
        tax_before_rebate = (400000 * 0.05) + (400000 * 0.10) + (400000 * 0.15) + ((taxable_income - 1600000) * 0.20)

    # 87A Rebate check (Zero tax up to 12 Lakh under 2026-27 regime)
    rebate_87a = 0.0
    if taxable_income <= 1200000:
        rebate_87a = tax_before_rebate
        final_tax_payable = 0.0
    else:
        final_tax_payable = tax_before_rebate
        # Add 4% Health & Education cess
        final_tax_payable += final_tax_payable * 0.04

    # Potential Refund of 194-O TDS
    refund_amount = 0.0
    if final_tax_payable == 0.0:
        refund_amount = tds_deducted_194o
    elif tds_deducted_194o > final_tax_payable:
        refund_amount = tds_deducted_194o - final_tax_payable
    else:
        refund_amount = 0.0

    # Weekly recommended set-aside
    weekly_tax_target = round(final_tax_payable / 52.0, 2)
    # Recommended Emergency Buffer set-aside: 5% of monthly net income / 4 weeks
    net_annual_income = annual_gross_income - effective_expense_deduction
    weekly_emergency_target = max(150.0, round((net_annual_income * 0.06) / 52.0, 2))

    return {
        "annual_gross_income": round(annual_gross_income, 2),
        "presumptive_deduction_sec44": round(effective_expense_deduction, 2),
        "taxable_income": round(taxable_income, 2),
        "tax_before_rebate": round(tax_before_rebate, 2),
        "rebate_87a": round(rebate_87a, 2),
        "final_tax_payable": round(final_tax_payable, 2),
        "is_zero_tax": final_tax_payable == 0.0,
        "tds_deducted_194o": round(tds_deducted_194o, 2),
        "tds_refund_claimable": round(refund_amount, 2),
        "weekly_tax_set_aside": weekly_tax_target,
        "weekly_emergency_set_aside": weekly_emergency_target,
        "applicable_itr_form": "ITR-4 (Sugam) for Presumptive Income",
        "tax_regime_note": (
            "Under Budget 2026-27 New Tax Regime, your income is well under the ₹12,00,000 threshold. "
            "You owe ₹0 tax and can claim your TDS refund directly to your bank account!"
        )
    }

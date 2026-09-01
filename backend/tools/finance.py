import json
from pathlib import Path
from typing import Dict, Any, List
from policy.policy_engine import check_payment

DEMO_DATA_DIR = Path(__file__).parent.parent.parent / "demo_data"

def list_pending_invoices() -> List[Dict[str, Any]]:
    invoices_file = DEMO_DATA_DIR / "invoices.json"
    if not invoices_file.exists():
        return []
    try:
        with open(invoices_file, "r") as f:
            data = json.load(f)
            invoices = data if isinstance(data, list) else [data]
            return [inv for inv in invoices if inv.get("status") == "pending"]
    except Exception:
        return []

def get_invoice(invoice_id: str) -> Dict[str, Any]:
    invoices_file = DEMO_DATA_DIR / "invoices.json"
    if not invoices_file.exists():
        return {}
    try:
        with open(invoices_file, "r") as f:
            data = json.load(f)
            invoices = data if isinstance(data, list) else [data]
            for inv in invoices:
                if inv.get("invoice_id") == invoice_id:
                    return inv
            return {}
    except Exception:
        return {}

def check_policy(vendor: str, amount: int) -> Dict[str, Any]:
    return check_payment(vendor, amount)

def propose_payment(invoice_id: str) -> Dict[str, Any]:
    invoice = get_invoice(invoice_id)
    if not invoice:
        return {"error": "Invoice not found"}
    policy_result = check_policy(invoice.get("vendor", ""), invoice.get("amount", 0))
    return {
        "invoice_id": invoice_id,
        "vendor": invoice.get("vendor"),
        "amount": invoice.get("amount"),
        "currency": invoice.get("currency", "INR"),
        "policy": policy_result
    }

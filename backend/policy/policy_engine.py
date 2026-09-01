from typing import Dict, Any

POLICY_CONFIG = {
    "max_transaction": 5000,
    "approved_vendors": [
        "Acme Supplies",
        "Office Depot"
    ],
    "require_approval": True
}

def check_payment(vendor: str, amount: int) -> Dict[str, Any]:
    vendor_approved = vendor in POLICY_CONFIG["approved_vendors"]
    within_limit = amount <= POLICY_CONFIG["max_transaction"]
    
    result = "DENY"
    if vendor_approved and within_limit:
        if POLICY_CONFIG["require_approval"]:
            result = "APPROVAL_REQUIRED"
        else:
            result = "ALLOW"
            
    return {
        "result": result,
        "vendor_approved": vendor_approved,
        "within_limit": within_limit,
        "limit": POLICY_CONFIG["max_transaction"]
    }

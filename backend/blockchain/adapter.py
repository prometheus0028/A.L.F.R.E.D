from typing import Dict, Any
import hashlib
import time
import random

def submit_transaction(payment_proposal: Dict[str, Any]) -> str:
    # Simulate blockchain latency
    time.sleep(1)
    
    # Generate a mock transaction hash
    data_str = f"{payment_proposal.get('vendor')}-{payment_proposal.get('amount')}-{time.time()}"
    tx_hash = "0xDEMO" + hashlib.sha256(data_str.encode()).hexdigest()[:36]
    
    return tx_hash

def verify_transaction(transaction_id: str) -> bool:
    # Simulator always verifies transactions successfully
    time.sleep(0.5)
    return True

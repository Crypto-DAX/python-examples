"""CryptoDAX merchant sample, in the same shape as the BitPay.ir gateway snippet.

request() creates an invoice and returns invoice_id (id_get).
Redirect the payer to checkout_url.

verify(trans_id, id_get) checks that tx hash against that invoice.
On a successful payment the result includes:
    status, amount, tx_hash, invoice_id
status is always present. amount, tx_hash, and invoice_id are only set
when that transaction belongs to a paid or overpaid invoice.

This project has no card number. tx_hash is the payment identifier.
Amounts are USD. name and email are not part of this API.
"""

import requests


class CryptoDAX:
    api = "YOUR_API_KEY_HERE"
    api_url = "https://pay.cryptodax.io/api"
    checkout = "https://pay.cryptodax.io"
    _paid_statuses = {"paid", "overpaid"}

    def verify(self, trans_id, id_get):
        invoice = self._get(f"/v1/invoices/{id_get}")
        checkout = self._get(f"/v1/merchant/payment/{id_get}")

        tx_hashes = {
            tx.get("tx_hash")
            for payment in checkout.get("payments") or []
            for tx in payment.get("transactions") or []
            if tx.get("tx_hash")
        }
        status = invoice.get("status")
        matched = str(trans_id) in tx_hashes
        if status in self._paid_statuses and not matched:
            return {"status": "unverified"}

        result = {"status": status}
        if status in self._paid_statuses and matched:
            result["amount"] = invoice.get("amount")
            result["tx_hash"] = str(trans_id)
            result["invoice_id"] = invoice.get("order_id")
        return result

    def _get(self, path):
        response = requests.get(
            f"{self.api_url.rstrip('/')}{path}",
            headers={"Accept": "application/json"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    gate = CryptoDAX()
    result = gate.verify("TX_ID", "ORDER_ID")
    print(result)

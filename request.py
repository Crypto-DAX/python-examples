import uuid

import requests


class CryptoDAX:
    api = "YOUR_API_KEY_HERE"
    api_url = "https://pay.cryptodax.io/api"
    redirect = "YOUR_REDIRECT_HERE"
    # redirect = "https://webhook.site/0fc48e29-3040-4b30-abe6-64c62f538686"

    def request(self, amount, order_id, description):
        data = {
            "amount": str(amount),
            "currency": "USD",
            "order_id": str(order_id),
            "description": description,
            "callback_url": self.redirect,
            "expire_minutes": 30,
        }

        response = requests.post(
            self.api_url + "/v1/invoices",
            json=data,
            headers={
                "Authorization": "Bearer " + self.api,
                "Accept": "application/json",
            },
        )
        return response

if __name__ == "__main__":
    gateCall = CryptoDAX()
    sample_order_id = uuid.uuid4().hex
    respond = gateCall.request(10000, sample_order_id, "optional")
    if respond.status_code == 201:
        print(respond.json())
        id_get = respond.json()["invoice_id"]
        # ### redirect user to  => https://pay.cryptodax.io/invoice/{id_get}
        print(f"https://pay.cryptodax.io/invoice/{id_get}")
    else:
        print(respond.status_code)
        print(respond.json())

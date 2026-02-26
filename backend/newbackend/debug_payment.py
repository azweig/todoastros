import requests
import json

BASE_URL = "https://api.todoastros.com"
api_key = "a56d089d-b0d3-46d7-999e-d2174b04d953"

payment_data = {
    "product_type": "premium_monthly",
    "quantity": 1
}

headers = {
    "Content-Type": "application/json",
    "X-API-Key": api_key
}

print("Enviando solicitud a:", f"{BASE_URL}/api/payment/create-checkout-session")
print("Headers:", json.dumps(headers, indent=2))
print("Datos:", json.dumps(payment_data, indent=2))

try:
    response = requests.post(
        f"{BASE_URL}/api/payment/create-checkout-session",
        headers=headers,
        json=payment_data
    )

    print("Código de respuesta:", response.status_code)
    print("Respuesta:", response.text)
except Exception as e:
    print("Error:", str(e))

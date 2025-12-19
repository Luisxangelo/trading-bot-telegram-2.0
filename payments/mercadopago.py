import mercadopago
from config import MERCADOPAGO_ACCESS_TOKEN, VIP_PRICE_USD

sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)

def create_payment_link(user_id: int, username: str):
    preference_data = {
        "items": [
            {
                "title": "Acceso VIP Señales Trading (30 días)",
                "quantity": 1,
                "unit_price": float(VIP_PRICE_USD),  # 🔴 IMPORTANTE
                "currency_id": "USD"
            }
        ],
        "external_reference": str(user_id),
        "auto_return": "approved",
        "back_urls": {
            "success": "https://google.com",
            "failure": "https://google.com",
            "pending": "https://google.com"
        }
    }

    preference = sdk.preference().create(preference_data)

    # 🔍 DEBUG CLARO (esto te ayudará siempre)
    if "response" not in preference:
        raise Exception(f"MercadoPago error: {preference}")

    response = preference["response"]

    if "init_point" not in response:
        raise Exception(f"MercadoPago response sin init_point: {response}")

    return response["init_point"]

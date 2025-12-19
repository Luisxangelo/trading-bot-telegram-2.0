import mercadopago
from config import MERCADOPAGO_ACCESS_TOKEN, VIP_PRICE_USD

sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)

def create_payment_link(user_id: int, username: str):
    preference_data = {
        "items": [
            {
                "title": "Acceso VIP Señales Trading (30 días)",
                "quantity": 1,
                "unit_price": VIP_PRICE_USD
            }
        ],
        "external_reference": str(user_id),
        "auto_return": "approved",
    }

    preference = sdk.preference().create(preference_data)
    return preference["response"]["init_point"]

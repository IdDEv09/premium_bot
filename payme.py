from fastapi import APIRouter, Header, HTTPException
import base64
from payments import give_product
from db import get_order

router = APIRouter()

PAYME_LOGIN = "Paycom"
PAYME_PASSWORD = "SECRET_KEY"

def verify_payme(auth: str):
    if not auth:
        raise HTTPException(status_code=401, detail="No auth header")
    try:
        decoded = base64.b64decode(auth.split(" ")[1]).decode()
        login, password = decoded.split(":")
    except:
        raise HTTPException(status_code=401, detail="Invalid auth")
    if login != PAYME_LOGIN or password != PAYME_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.post("/payme/webhook")
async def payme_webhook(data: dict, authorization: str = Header(None)):
    verify_payme(authorization)
    order_id = int(data["account"]["order_id"])
    await give_product(order_id)
    return {"result": "ok"}

@router.post("/api/payme/create")
async def create_payme(data: dict):
    order_id = data["order_id"]
    order = await get_order(order_id)
    if not order:
        return {"error": "order not found"}

    amount = order[4] * 100
    pay_url = f"https://checkout.paycom.uz/{PAYME_LOGIN}?amount={amount}&account[order_id]={order_id}"
    return {"pay_url": pay_url}
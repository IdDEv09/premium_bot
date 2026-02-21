from fastapi import FastAPI, Request
from aiogram.types import Update
from bot import bot, dp
from payme import router as payme_router

app = FastAPI()
app.include_router(payme_router)
@app.get("/")
async def root():
    return {"message": "Bot ishlayapti 🚀"}

@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)

    return {"ok": True}

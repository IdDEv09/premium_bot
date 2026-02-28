from fastapi import FastAPI, Request
from aiogram.types import Update
from starlette.middleware.base import DispatchFunction

from bot import bot, dp
from payme import router as payme_router
import aiosqlite

async def init_db():
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            product TEXT,
            amount INTEGER,
            status TEXT
        )
        """)
        await db.commit()
app = FastAPI()
app.include_router(payme_router)
@app.get("/telegram/webhook")
async def test():
    return {"status": "webhook ishlayapti"}
@app.get("/")
async def root():
    return {"message": "Bot ishlayapti 🚀"}
@app.post("/api/payme/create")
async def create_payme(data: dict):
    # Payme integratsiyasi uchun kod
    ...
@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

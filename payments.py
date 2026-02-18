from db import get_order, set_order_done
from bot import bot, ADMIN_ID

async def give_product(order_id: int):
    order = await get_order(order_id)
    if not order:
        return

    _, user_id, username, product, amount, status = order

    if status == "done":
        return

    # Foydalanuvchiga xabar
    await bot.send_message(
        user_id,
        f"✅ To‘lov qabul qilindi!\n⏳ {product} buyurtmangiz 1–5 daqiqa ichida beriladi."
    )

    # Admin xabari
    await bot.send_message(
        ADMIN_ID,
        f"🟢 TO‘LOV TASDIQLANDI\n"
        f"🆔 Order #{order_id}\n"
        f"📦 {product}\n"
        f"👤 @{username}\n"
        f"💰 {amount} so‘m\n\n➡️ Fragment orqali yuboring"
    )

    await set_order_done(order_id)
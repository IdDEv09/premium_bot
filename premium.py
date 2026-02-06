import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from db import create_order

# ================== SOZLAMALAR ==================
TOKEN = "8221602548:AAHzxCEaxOGF4h9x3ySY-25lib5n3evgNNQ"
ADMIN_USERNAME = "isr0049"
ADMIN_ID = 8001913525
CHANNEL = "@a1withus"  # Kanal username yoki private ID

bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ================== NARXLAR ==================
PRICES = {
    # Premium
    "1 oy Premium - 40k": 40000,
    "3 oy Premium - 100k": 100000,
    "6 oy Premium - 180k": 180000,
    "12 oy Premium - 300k": 300000,
    # Stars
    "50 ⭐️ - 10k": 10000,
    "100 ⭐️ - 18k": 18000,
    "250 ⭐️ - 40k": 40000,
    "500 ⭐️ - 75k": 75000,
    "1000 ⭐️ - 140k": 140000,
    "1500 ⭐️ - 200k": 200000,
    "2000 ⭐️ - 280k": 280000,
    "3000 ⭐️ - 380k": 380000,
    # Gifts
    "❤️ Yurak - 5k": 5000,
    "🧸 Ayiqcha - 15k": 15000,
    "🌹 Atirgul - 10k": 10000,
    "🎂 Tort - 20k": 20000,
    "💐 Guldasta - 25k": 25000,
    "🚀 Raketa - 30k": 30000,
    "💍 Uzuk - 50k": 50000,
    "💎 Diamond - 100k": 100000,
}

# ================== MENULAR ==================
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⭐️ Premium"), KeyboardButton(text="⭐️ Stars")],
            [KeyboardButton(text="🎁 Gift"), KeyboardButton(text="👤 Admin bilan bog‘lanish")]
        ], resize_keyboard=True
    )

def premium_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1 oy Premium - 40k")],
            [KeyboardButton(text="3 oy Premium - 100k")],
            [KeyboardButton(text="6 oy Premium - 180k")],
            [KeyboardButton(text="12 oy Premium - 300k")],
            [KeyboardButton(text="🔙 Orqaga")]
        ], resize_keyboard=True
    )

def stars_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="50 ⭐️ - 10k"), KeyboardButton(text="100 ⭐️ - 18k")],
            [KeyboardButton(text="250 ⭐️ - 40k"), KeyboardButton(text="500 ⭐️ - 75k")],
            [KeyboardButton(text="1000 ⭐️ - 140k"), KeyboardButton(text="1500 ⭐️ - 200k")],
            [KeyboardButton(text="2000 ⭐️ - 280k"), KeyboardButton(text="3000 ⭐️ - 380k")],
            [KeyboardButton(text="🔙 Orqaga")]
        ], resize_keyboard=True
    )

def gift_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❤️ Yurak - 5k"), KeyboardButton(text="🧸 Ayiqcha - 15k")],
            [KeyboardButton(text="🌹 Atirgul - 10k"), KeyboardButton(text="🎂 Tort - 20k")],
            [KeyboardButton(text="💐 Guldasta - 25k"), KeyboardButton(text="🚀 Raketa - 30k")],
            [KeyboardButton(text="💍 Uzuk - 50k"), KeyboardButton(text="💎 Diamond - 100k")],
            [KeyboardButton(text="🔙 Orqaga")]
        ], resize_keyboard=True
    )

subscribe_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📢 Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL}")],
        [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]
    ]
)

# ================== FSM ==================
class BuyState(StatesGroup):
    waiting_username = State()

# ================== OBUNA TEKSHIRUV ==================
async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        return member.status in ["creator", "administrator", "member"]
    except Exception as e:
        logging.warning(f"Obuna tekshirish xatosi: {e}")
        return False

# ================== START ==================
@dp.message(CommandStart())
async def start_cmd(message: Message):
    if await check_subscription(message.from_user.id):
        await message.answer("✅ Obuna tasdiqlandi! Kerakli bo‘limni tanlang 👇", reply_markup=main_menu())
    else:
        await message.answer("❌ Botdan foydalanish uchun kanalimizga obuna bo‘ling:", reply_markup=subscribe_kb)

# ================== TEKSHIRISH TUGMASI ==================
@dp.callback_query(F.data == "check_sub")
async def check_sub_cb(c):
    if await check_subscription(c.from_user.id):
        await c.message.answer("✅ Obuna tasdiqlandi! Kerakli bo‘limni tanlang:", reply_markup=main_menu())
        await c.answer()
    else:
        await c.answer("❌ Siz hali obuna bo‘lmadingiz!", show_alert=True)

# ================== BO‘LIMLAR ==================
@dp.message(F.text == "⭐️ Premium")
async def premium_section(message: Message):
    if not await check_subscription(message.from_user.id):
        await message.answer("❌ Kanalga obuna bo‘lishingiz shart!", reply_markup=subscribe_kb)
        return
    await message.answer("Premium tanlang:", reply_markup=premium_menu())

@dp.message(F.text == "⭐️ Stars")
async def stars_section(message: Message):
    if not await check_subscription(message.from_user.id):
        await message.answer("❌ Kanalga obuna bo‘lishingiz shart!", reply_markup=subscribe_kb)
        return
    await message.answer("Stars tanlang:", reply_markup=stars_menu())

@dp.message(F.text == "🎁 Gift")
async def gift_section(message: Message):
    if not await check_subscription(message.from_user.id):
        await message.answer("❌ Kanalga obuna bo‘lishingiz shart!", reply_markup=subscribe_kb)
        return
    await message.answer("Gift tanlang:", reply_markup=gift_menu())

@dp.message(F.text == "👤 Admin bilan bog‘lanish")
async def contact_admin(message: Message):
    await message.answer(f"Admin bilan bog‘lanish: https://t.me/{ADMIN_USERNAME}")

@dp.message(F.text == "🔙 Orqaga")
async def back_main(message: Message):
    await message.answer("Asosiy menyu", reply_markup=main_menu())

# ================== BUYURTMA ==================
orders = {}
order_id_seq = 1

@dp.message(F.text.in_(PRICES.keys()))
async def ask_username(message: Message, state: FSMContext):
    global order_id_seq
    product = message.text
    await state.update_data(product=product)

    # 1 oylik Premium → faqat admin
    if "1 oy Premium" in product:
        await message.answer(f"1 oylik premium faqat admin orqali beriladi.\n👉 https://t.me/{ADMIN_USERNAME}")
        # Adminga xabar
        await bot.send_message(ADMIN_ID, f"❗️ Foydalanuvchi @{message.from_user.username} 1 oylik Premium olishni xohladi.")
        return

    await message.answer("Kim uchun? (@username kiriting)")
    await state.set_state(BuyState.waiting_username)

@dp.message(BuyState.waiting_username)
async def process_username(message: Message, state: FSMContext):
    global order_id_seq
    data = await state.get_data()
    product = data["product"]
    username = message.text.replace("@", "")
    price = PRICES[product]

    oid = order_id_seq
    order_id_seq += 1

    orders[oid] = {
        "user_id": message.from_user.id,
        "username": username,
        "product": product,
        "amount": price,
        "status": "pending"
    }

    # To‘lov linklari
    payme_url = f"https://checkout.paycom.uz/YOUR_PAYME_MERCHANT?amount={price*100}&account[order_id]={oid}"
    miniapp_url = f"https://YOURDOMAIN.uz/miniapp/index.html?order_id={oid}"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Karta orqali to‘lov", url=miniapp_url)],
        [InlineKeyboardButton(text="💳 Payme orqali to‘lov", url=payme_url)]
    ])

    await message.answer(
        f"🧾 Buyurtma #{oid}\n{product}\n👤 @{username}\n\nTo‘lov uchun bosing 👇",
        reply_markup=kb
    )

    await bot.send_message(ADMIN_ID, f"🆕 Buyurtma #{oid}\n{product}\n@{username}")
    await state.clear()

# ================== MAHSULOT BERISH ==================
async def give_product(order_id: int):
    order = orders.get(order_id)
    if not order or order["status"] == "done":
        return
    user_id = order["user_id"]
    product = order["product"]
    await bot.send_message(user_id, f"✅ Buyurtma tasdiqlandi! Sizga berildi: {product}")
    orders[order_id]["status"] = "done"

# ================== RUN ==================
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

# ================== SOZLAMALAR ==================
TOKEN = "8221602548:AAHyjvsXMr5LdLksEtbyEvTMSygS3Gduvsg"
ADMIN_USERNAME = "isr0049"
ADMIN_ID = 8001913525
CHANNEL = "@a1withus"

bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ================== NARXLAR ==================
PRICES = {
    "1 oy Premium - 40k": 40000,
    "3 oy Premium - 165k": 165000,
    "6 oy Premium - 220k": 220000,
    "12 oy Premium - 395k": 395000,
    "50 ⭐️ - 10k": 10000,
    "100 ⭐️ - 20k": 20000,
    "250 ⭐️ - 49k": 49000,
    "500 ⭐️ - 99k": 99000,
    "1000 ⭐️ - 195k": 195000,
    "1500 ⭐️ - 290k": 290000,
    "2500 ⭐️ - 480k": 480000,
    "5000 ⭐️ - 950k": 950000,
    "❤️ Yurak - 3k": 3000,
    "🧸 Ayiqcha - 3k": 3000,
    "🌹 Atirgul - 5k": 5000,
    "🎂 Tort - 5k": 5000,
    "💐 Guldasta - 10k": 10000,
    "🚀 Raketa - 10k": 10000,
    "💍 Uzuk - 20k": 20000,
    "💎 Diamond - 20k": 20000,
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
            [KeyboardButton(text="3 oy Premium - 165k")],
            [KeyboardButton(text="6 oy Premium - 220k")],
            [KeyboardButton(text="12 oy Premium - 395k")],
            [KeyboardButton(text="🔙 Orqaga")]
        ], resize_keyboard=True
    )

def stars_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="50 ⭐️ - 10k"), KeyboardButton(text="100 ⭐️ - 20k")],
            [KeyboardButton(text="250 ⭐️ - 49k"), KeyboardButton(text="500 ⭐️ - 99k")],
            [KeyboardButton(text="1000 ⭐️ - 195k"), KeyboardButton(text="1500 ⭐️ - 290k")],
            [KeyboardButton(text="2500 ⭐️ - 480k"), KeyboardButton(text="5000 ⭐️ - 950k")],
            [KeyboardButton(text="🔙 Orqaga")]
        ], resize_keyboard=True
    )

def gift_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❤️ Yurak - 3k"), KeyboardButton(text="🧸 Ayiqcha - 3k")],
            [KeyboardButton(text="🌹 Atirgul - 5k"), KeyboardButton(text="🎂 Tort - 5k")],
            [KeyboardButton(text="💐 Guldasta - 10k"), KeyboardButton(text="🚀 Raketa - 10k")],
            [KeyboardButton(text="💍 Uzuk - 20k"), KeyboardButton(text="💎 Diamond - 20k")],
            [KeyboardButton(text="🔙 Orqaga")]
        ], resize_keyboard=True
    )

subscribe_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📢 Kanalga obuna bo‘lish", url="https://t.me/a1withus")],
        [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]
    ]
)

# ================== FSM ==================
class BuyState(StatesGroup):
    waiting_username = State()
    choosing_recipient = State()

# ================== OBUNA TEKSHIRUV ==================
async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        return member.status in ["creator", "administrator", "member"]
    except:
        return False

# ================== START ==================
@dp.message(CommandStart())
async def start_cmd(message: Message):
    if await check_subscription(message.from_user.id):
        await message.answer("✅ Obuna tasdiqlandi!", reply_markup=main_menu())
    else:
        await message.answer("❌ Kanalga obuna bo‘ling:", reply_markup=subscribe_kb)

# ================== BUYURTMA ==================
orders = {}
order_id_seq = 1

@dp.message(F.text.in_(PRICES.keys()))
async def ask_recipient(message: Message, state: FSMContext):
    product = message.text

    if "1 oy Premium" in product:
        await message.answer(f"1 oylik Premium faqat admin orqali:\nhttps://t.me/{ADMIN_USERNAME}")
        return

    await state.update_data(product=product)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="O'zimga", callback_data="to_self"),
         InlineKeyboardButton(text="Boshqasiga", callback_data="to_other")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")]
    ])

    await message.answer("Kim uchun?", reply_markup=kb)
    await state.set_state(BuyState.choosing_recipient)

@dp.callback_query(F.data.in_({"to_self", "to_other", "back"}))
async def choose_recipient_cb(c, state: FSMContext):
    global order_id_seq

    if c.data == "back":
        await c.message.answer("Asosiy menyu", reply_markup=main_menu())
        await state.clear()
        return

    data = await state.get_data()
    product = data["product"]
    price = PRICES[product]

    if c.data == "to_other":
        await c.message.answer("Username kiriting (@siz):")
        await state.set_state(BuyState.waiting_username)
        return

    username = c.from_user.username or str(c.from_user.id)

    oid = order_id_seq
    order_id_seq += 1

    orders[oid] = {
        "user_id": c.from_user.id,
        "username": username,
        "product": product,
        "amount": price,
        "status": "pending"
    }

    payme_url = f"https://merchant.payme.uz/business/697b7d32c4a421a1da3e393b?amount={price*100}&account[order_id]={oid}"
    miniapp_url = f"https://premium-bot-9i2r.onrender.com/miniapp/index.html?order_id={oid}"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Karta orqali to‘lov", url=miniapp_url)],
        [InlineKeyboardButton(text="💳 Payme orqali to‘lov", url=payme_url)]
    ])

    await c.message.answer(
        f"🧾 Buyurtma #{oid}\n{product}\n👤 @{username}",
        reply_markup=kb
    )

    await bot.send_message(ADMIN_ID, f"🆕 Buyurtma #{oid}\n{product}\n@{username}")
    await state.clear()

@dp.message(BuyState.waiting_username)
async def process_username(message: Message, state: FSMContext):
    global order_id_seq

    data = await state.get_data()
    product = data["product"]
    price = PRICES[product]
    username = message.text.replace("@", "").strip()

    oid = order_id_seq
    order_id_seq += 1

    orders[oid] = {
        "user_id": message.from_user.id,
        "username": username,
        "product": product,
        "amount": price,
        "status": "pending"
    }

    payme_url = f"https://merchant.payme.uz/business/697b7d32c4a421a1da3e393b?amount={price*100}&account[order_id]={oid}"
    miniapp_url = f"https://premium-bot-9i2r.onrender.com/miniapp/index.html?order_id={oid}"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Karta orqali to‘lov", url=miniapp_url)],
        [InlineKeyboardButton(text="💳 Payme orqali to‘lov", url=payme_url)]
    ])

    await message.answer(
        f"🧾 Buyurtma #{oid}\n{product}\n👤 @{username}",
        reply_markup=kb
    )

    await bot.send_message(ADMIN_ID, f"🆕 Buyurtma #{oid}\n{product}\n@{username}")
    await state.clear()

# ================== RUN ==================
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
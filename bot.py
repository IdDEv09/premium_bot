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
CHANNEL = "@a1withus"  # Kanal username yoki private ID

bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ================== NARXLAR ==================
PRICES = {
    # Premium
    "1 oy Premium - 40k": 40000,
    "3 oy Premium - 165k": 165000,
    "6 oy Premium - 220k": 220000,
    "12 oy Premium - 395k": 395000,
    # Stars
    "50 ⭐️ - 10k": 10000,
    "100 ⭐️ - 20k": 20000,
    "250 ⭐️ - 49k": 49000,
    "500 ⭐️ - 99k": 99000,
    "1000 ⭐️ - 195k": 195000,
    "1500 ⭐️ - 290k": 290000,
    "2500 ⭐️ - 480k": 480000,
    "5000 ⭐️ - 950k": 950000,
    # Gifts
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
        [InlineKeyboardButton(text="📢 Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL}")],
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
async def ask_recipient(message: Message, state: FSMContext):
    global order_id_seq
    product = message.text

    # 1 oylik premium faqat admin orqali
    if "1 oy Premium" in product:
        await message.answer(f"1 oylik Premium faqat admin orqali beriladi.\n👉 https://t.me/{ADMIN_USERNAME}")
        await bot.send_message(ADMIN_ID, f"❗️ @{message.from_user.username} 1 oylik Premium olishni xohladi.")
        return

    await state.update_data(product=product)
    await message.answer("Kim uchun olmoqchisiz?", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="O'zimga", callback_data="to_self"),
             InlineKeyboardButton(text="Boshqasiga", callback_data="to_other")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")]
        ]
    ))
    await state.set_state(BuyState.choosing_recipient)

@dp.callback_query(F.data.in_({"to_self", "to_other"}))
async def choose_recipient_cb(c, state: FSMContext):
    data = await state.get_data()
    product = data["product"]
    price = PRICES[product]

    global order_id_seq
    oid = order_id_seq
    order_id_seq += 1

    if c.data == "to_self":
        username = c.from_user.username
    else:
        await c.message.answer("Iltimos, foydalanuvchi @username kiriting:")
        await state.set_state(BuyState.waiting_username)
        return

    orders[oid] = {
        "user_id": c.from_user.id,
        "username": username,
        "product": product,
        "amount": price,
        "status": "pending"
    }

    # To‘lov linklari
    payme_url = f"https://merchant.payme.uz/business/697b7d32c4a421a1da3e393b?amount={price*100}&account[order_id]={oid}"
    miniapp_url = f"https://premium-bot-9i2r.onrender.com/miniapp/index.html?order_id={oid}"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Karta orqali to‘lov", url=miniapp_url)],
        [InlineKeyboardButton(text="💳 Payme orqali to‘lov", url=payme_url)]
    ])

    await c.message.answer(
        f"🧾 Buyurtma #{oid}\n{product}\n👤 @{username}\n\nTo‘lov uchun bosing 👇",
        reply_markup=kb
    )

    await bot.send_message(ADMIN_ID, f"🆕 Buyurtma #{oid}\n{product}\n@{username}")
    await state.clear()

@dp.message(BuyState.waiting_username)
async def process_username(message: Message, state: FSMContext):
    data = await state.get_data()
    product = data["product"]
    username = message.text.replace("@", "")
    price = PRICES[product]

    global order_id_seq
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
    payme_url = f"https://merchant.payme.uz/business/697b7d32c4a421a1da3e393b?amount={price*100}&account[order_id]={oid}"
    miniapp_url = f"https://premium-bot-9i2r.onrender.com/miniapp/index.html?order_id={oid}"

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
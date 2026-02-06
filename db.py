import aiosqlite

DB_NAME = "database.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
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

async def create_order(user_id, username, product, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute(
            "INSERT INTO orders (user_id, username, product, amount, status) VALUES (?,?,?,?,?)",
            (user_id, username, product, amount, "pending")
        )
        await db.commit()
        return cur.lastrowid

async def get_order(order_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute("SELECT * FROM orders WHERE id=?", (order_id,))
        return await cur.fetchone()

async def set_order_done(order_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE orders SET status='done' WHERE id=?", (order_id,))
        await db.commit()
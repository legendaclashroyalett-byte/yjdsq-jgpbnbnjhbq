import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# ======= Flask для аптайма =======
app = Flask('')

@app.route('/')
def home():
    return "Бот онлайн ✅"

def run():
    port = int(os.environ.get("PORT", 8080))  # Replit задаёт свой PORT
    app.run(host="0.0.0.0", port=port)

# Запускаем Flask в отдельном потоке
t = Thread(target=run)
t.start()

# ======= Телеграм токен из Replit Secrets =======
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")  # <--- убрали ""

if not TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN environment variable is not set")
    exit(1)

# ======= Список товаров =======
products = {
    "1": {"name": "Буст Андроид", "price": 40, "link": "https://telegra.ph/Optimizaciya-bust-FPS-ANDROID-05-22"},
    "2": {"name": "Буст IOS", "price": 40, "link": "https://telegra.ph/Optimizaciya-bust-FPS-IPHONE-05-22"},
    "3": {"name": "Буст ПК", "price": 100, "link": "https://telegra.ph/Povyshenie-FPS-Vo-Vseh-Igrah-05-06"},
    "4": {"name": "Все приложения от Adobe", "price": 20, "link": "https://telegra.ph/Vse-prilozheniya-ot-Adobe-12-21"},
    "16": {"name": "99к игр STEAM", "price": 500, "link": "https://telegra.ph/Steam-05-22-24"}
}

# ======= Инициализация бота =======
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ======= Главное меню =======
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛍 Каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="ℹ️ Информация", callback_data="info")]
    ])

# ======= Каталог =======
def catalog_menu():
    keyboard = []
    for pid, p in products.items():
        keyboard.append([InlineKeyboardButton(
            text=f"🛒 {p['name']} — {p['price']}⭐",
            callback_data=f"buy_{pid}"
        )])
    keyboard.append([InlineKeyboardButton(text="⬅ Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# ======= Старт =======
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать!\nВыберите действие 👇",
        reply_markup=main_menu()
    )

# ======= Каталог =======
@dp.callback_query(lambda c: c.data == "catalog")
async def catalog(callback: types.CallbackQuery):
    await callback.message.answer(
        "🛍 Каталог товаров:",
        reply_markup=catalog_menu()
    )

# ======= Информация =======
@dp.callback_query(lambda c: c.data == "info")
async def info(callback: types.CallbackQuery):
    await callback.message.answer(
        "ℹ️ Оплата через Telegram Stars.\nТовар приходит автоматически."
    )

# ======= Покупка =======
@dp.callback_query(lambda c: c.data.startswith("buy_"))
async def buy(callback: types.CallbackQuery):
    pid = callback.data.split("_")[1]
    product = products[pid]
    await callback.message.answer(f"✅ Вы выбрали: {product['name']}\nСсылка: {product['link']}")

# ======= Основной цикл =======
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


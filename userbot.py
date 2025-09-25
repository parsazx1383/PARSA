import asyncio
import json
import random
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineQueryResultArticle, InputTextMessageContent

# تنظیمات اولیه (جایگزین کن)
api_id = 28285817  # از my.telegram.org
api_hash = "5c96b16dea2daf25995ef30a02424bb9"
session_name = "userbot_session"

# فونت‌های ساعت (اعداد unicode)
fonts = {
    "normal": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "bold": ["𝟎", "𝟏", "𝟐", "𝟑", "𝟒", "𝟓", "𝟔", "𝟕", "𝟖", "𝟗"],
    "circle": ["⓪", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨"],
    "random": ["random"]  # برای انتخاب تصادفی
}

# تابع برای لود و سیو تنظیمات
def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        default = {
            "secretary_on": False,
            "secretary_text": "سلام، الان مشغولم! بعدا پیام بدید.",
            "delay": 5,
            "clock_on": False,
            "clock_font": "bold",
            "bold_mode": False
        }
        save_settings(default)
        return default

def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f)

app = Client(session_name, api_id=api_id, api_hash=api_hash)

# هندلر برای secretary (پاسخ خودکار)
@app.on_message(filters.private & ~filters.me & filters.incoming)
async def secretary_handler(client, message: Message):
    settings = load_settings()
    if settings["secretary_on"]:
        await asyncio.sleep(settings["delay"])
        text = settings["secretary_text"]
        if settings["bold_mode"]:
            text = f"**{text}**"
        await message.reply(text, parse_mode="markdown" if settings["bold_mode"] else None)

# لوپ برای ساعت در last_name
async def clock_loop():
    while True:
        settings = load_settings()
        if not settings["clock_on"]:
            await asyncio.sleep(60)
            continue
        now = datetime.now()
        hour = str(now.hour).zfill(2)
        minute = str(now.minute).zfill(2)
        font_name = settings["clock_font"]
        if font_name == "random":
            font_name = random.choice(["normal", "bold", "circle"])
        font = fonts.get(font_name, fonts["bold"])
        clock_str = "".join(font[int(d)] for d in hour + minute)
        await app.update_profile(last_name=clock_str)
        await asyncio.sleep(60)

# دستورات برای تغییر تنظیمات (از خود user)
@app.on_message(filters.me & filters.command("set_text", prefixes="."))
async def set_secretary_text(client, message: Message):
    text = " ".join(message.command[1:])
    if text:
        settings = load_settings()
        settings["secretary_text"] = text
        save_settings(settings)
        await message.reply("متن منشی تغییر کرد!")
    else:
        await message.reply("متن رو وارد کن: .set_text <text>")

@app.on_message(filters.me & filters.command("set_delay", prefixes="."))
async def set_delay(client, message: Message):
    try:
        delay = int(message.command[1])
        settings = load_settings()
        settings["delay"] = delay
        save_settings(settings)
        await message.reply(f"زمان تاخیر به {delay} ثانیه تغییر کرد!")
    except:
        await message.reply("عدد وارد کن: .set_delay <seconds>")

@app.on_message(filters.me & filters.command("set_font", prefixes="."))
async def set_font(client, message: Message):
    font = message.command[1].lower() if len(message.command) > 1 else ""
    if font in fonts:
        settings = load_settings()
        settings["clock_font"] = font
        save_settings(settings)
        await message.reply(f"فونت ساعت به {font} تغییر کرد!")
    else:
        await message.reply(f"فونت موجود: {', '.join(fonts.keys())}")

# دستور .پنل برای فراخوانی پنل از helper bot
@app.on_message(filters.me & filters.command("پنل", prefixes="."))
async def panel_command(client, message: Message):
    bot_username = "your_helper_bot_username"  # جایگزین کن با یوزرنیم helper bot، مثل @MyHelperBot
    try:
        results = await app.get_inline_bot_results(bot_username, "panel")
        if results.results:
            await app.send_inline_bot_result(
                chat_id=message.chat.id,
                query_id=results.query_id,
                result_id=results.results[0].id
            )
            await message.delete()
        else:
            await message.reply("هیچ نتیجه‌ای پیدا نشد!")
    except Exception as e:
        await message.reply(f"خطا: {str(e)}")

# استارت لوپ ساعت
asyncio.create_task(clock_loop())

app.run()
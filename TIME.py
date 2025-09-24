import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import time
import random
from datetime import datetime
import pytz

API_ID = 12429393
API_HASH = "2ec066334fb39f42e4ee8fbc5b640384"

app = Client("TG-PARSA", api_id=API_ID, api_hash=API_HASH)

# Define fonts for numbers
FONTS = [
    "0123456789",
    "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
    "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿",
    "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",
    "０１２３４５６７８９",
    "0̸1̸2̸3̸4̸5̸6̸7̸8̸9̸",
    "0҉1҉2҉3҉4҉5҉6҉7҉8҉9҉",
    "⓿➊➋➌➍➎➏➐➑➒",
    "⓪①②③④⑤⑥⑦⑧⑨",
    "੦౹੨੩੫ƼϬԴ੪੧",
    "⁰¹²³⁴⁵⁶⁷⁸⁹",
    "0͓̽1͓̽2͓̽3͓̽4͓̽5͓̽6͓̽7͓̽8͓̽9͓̽",
    "0⃗1⃗2⃗3⃗4⃗5⃗6⃗7⃗8⃗9⃗",
    "0͎1͎2͎3͎4͎5͎6͎7͎8͎9͎"
]

# Global variables
is_running = False
current_font_index = 0

# Convert number to selected font
def convert_to_font(time_str, font_index):
    font = FONTS[font_index]
    return ''.join(font[int(digit)] for digit in time_str if digit.isdigit())

# Update last name with current time
async def update_time():
    global is_running, current_font_index
    while is_running:
        tehran_tz = pytz.timezone('Asia/Tehran')
        current_time = datetime.now(tehran_tz).strftime("%H:%M")
        formatted_time = convert_to_font(current_time.replace(":", ""), current_font_index)
        formatted_time = f"{formatted_time[:2]}:{formatted_time[2:]}"
        try:
            await app.update_profile(last_name=f"{formatted_time}")
        except Exception as e:
            print(f"Error updating profile: {e}")
        await asyncio.sleep(60)  # Update every minute

# Command to enable time update
@app.on_message(filters.command("ساعت روشن", prefixes=".") & filters.me)
async def enable_time(client: Client, message: Message):
    global is_running
    if not is_running:
        is_running = True
        await message.edit_text("ساعت روشن شد✔️")
        asyncio.create_task(update_time())
    else:
        await message.edit_text("ساعت قبلاً روشن است!")

# Command to disable time update
@app.on_message(filters.command("ساعت خاموش", prefixes=".") & filters.me)
async def disable_time(client: Client, message: Message):
    global is_running
    if is_running:
        is_running = False
        await message.edit_text("ساعت خاموش شد✖️")
        await app.update_profile(last_name="")  # Clear last name
    else:
        await message.edit_text("ساعت قبلاً خاموش است!")

# Command to change font
@app.on_message(filters.command("فونت", prefixes=".") & filters.me)
async def change_font(client: Client, message: Message):
    global current_font_index
    try:
        args = message.text.split()
        if len(args) > 1:
            if args[1].lower() == "رندوم":
                current_font_index = random.randint(0, len(FONTS) - 1)
            else:
                font_index = int(args[1])
                if 0 <= font_index < len(FONTS):
                    current_font_index = font_index
                else:
                    await message.edit_text("شماره فونت نامعتبر است!")
                    return
        else:
            await message.edit_text("لطفاً شماره فونت یا 'رندوم' را مشخص کنید!")
            return
        await message.edit_text("فونت تغییر کرد✔️")
    except ValueError:
        await message.edit_text("لطفاً یک شماره فونت معتبر یا 'رندوم' وارد کنید!")

# Start the bot
app.run()
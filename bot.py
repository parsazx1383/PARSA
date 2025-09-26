import asyncio
import random
import json
import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import platform

# Client setup
api_id = 28285817  # Replace with your API ID
api_hash = '5c96b16dea2daf25995ef30a02424bb9'  # Replace with your API hash
session_name = 'VIP-TG'
device_model = "iPhone 8 Plus"
system_version = "IOS-16.7.10"
app_version = "IOS 16.7.10"
lang_code = "en"

app = Client(
    session_name,
    api_id,
    api_hash,
    device_model=device_model,
    system_version=system_version,
    app_version=app_version,
    lang_code=lang_code
)

# Data storage
muted_users = set()
enemies = set()
loves = set()
enemy_texts = ["کصخل", "بی شعور", "احمق"]  # Default enemy texts
default_enemy_texts = enemy_texts.copy()
love_texts = ["عزیزم", "قلبم", "دوستت دارم"]  # Default love texts
default_love_texts = love_texts.copy()
timename_enabled = False
timebio1_enabled = False
timebio2_enabled = False
antilogin_enabled = False
text_modes = {
    "bold": False,
    "spoiler": False,
    "italic": False,
    "code": False,
    "underline": False,
    "strike": False,
    "quote": False,
    "montion": False
}
current_font = "1"

# Font mappings
fonts = {
    "1": "0123456789",
    "2": "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
    "3": "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿",
    "4": "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",
    "5": "０１２３４５６７８９",
    "6": "0̸1̸2̸3̸4̸5̸6̸7̸8̸9̸",
    "7": "⓪①②③④⑤⑥⑦⑧⑨",
    "8": "⓿➊➋➌➍➎➏➐➑➒",
    "9": "੦౹੨੩੫ƼϬԴ੪੧",
    "10": "⁰¹²³⁴⁵⁶⁷⁸⁹",
    "11": "0͓̽1͓̽2͓̽3͓̽4͓̽5͓̽6͓̽7͓̽8͓̽9͓̽",
    "12": "0҈1҈2҈3҈4҈5҈6҈7҈8҈9҈",
    "13": "0⃗1⃗2⃗3⃗4⃗5⃗6⃗7⃗8⃗9⃗"
}

def convert_to_font(time_str, font_key):
    if font_key == "random":
        font_key = random.choice(list(fonts.keys()))
    font = fonts.get(font_key, fonts["1"])
    return ''.join(font[int(c)] if c.isdigit() else c for c in time_str)

async def update_timename():
    global timename_enabled
    while timename_enabled:
        current_time = datetime.now().strftime("%H:%M:%S")
        formatted_time = convert_to_font(current_time, current_font)
        await app.update_profile(last_name=formatted_time)
        await asyncio.sleep(1)

async def update_timebio():
    while timebio1_enabled or timebio2_enabled:
        current_time = datetime.now()
        date_str = current_time.strftime("%Y/%m/%d")
        time_str = current_time.strftime("%H:%M:%S")
        day_name = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یک‌شنبه"][current_time.weekday()]
        
        if timebio1_enabled:
            bio = f"✅ فضولی شما در تاریخ {date_str} ساعت {time_str} با موفقیت ثبت شد."
            await app.update_profile(bio=bio)
        
        if timebio2_enabled:
            bio = f"💚 | 𝙵❤️𝚅𝙴 | {time_str} | {date_str} | {day_name}"
            await app.update_profile(bio=bio)
        
        await asyncio.sleep(1)

# Mute commands
@app.on_message(filters.command("mute") & filters.reply)
async def mute_user(client, message: Message):
    user_id = message.reply_to_message.from_user.id
    muted_users.add(user_id)
    await message.reply("کاربر به حالت سکوت تغییر کرد.")

@app.on_message(filters.command("unmute") & filters.reply)
async def unmute_user(client, message: Message):
    user_id = message.reply_to_message.from_user.id
    muted_users.discard(user_id)
    await message.reply("کاربر از حالت سکوت خارج شد.")

@app.on_message(filters.command("mutelist"))
async def mute_list(client, message: Message):
    if muted_users:
        users = "\n".join([str(user_id) for user_id in muted_users])
        await message.reply(f"لیست کاربران در حالت سکوت:\n{users}")
    else:
        await message.reply("هیچ کاربری در حالت سکوت نیست.")

@app.on_message(filters.command("clearmutelist"))
async def clear_mute_list(client, message: Message):
    muted_users.clear()
    await message.reply("لیست کاربران در حالت سکوت پاک شد.")

# Enemy commands
@app.on_message(filters.command("setenemy") & filters.reply)
async def set_enemy(client, message: Message):
    user_id = message.reply_to_message.from_user.id
    enemies.add(user_id)
    await message.reply("کاربر به لیست دشمنان اضافه شد.")

@app.on_message(filters.command("delenemy") & filters.reply)
async def del_enemy(client, message: Message):
    user_id = message.reply_to_message.from_user.id
    enemies.discard(user_id)
    await message.reply("کاربر از لیست دشمنان خارج شد.")

@app.on_message(filters.command("enemylist"))
async def enemy_list(client, message: Message):
    if enemies:
        users = "\n".join([str(user_id) for user_id in enemies])
        await message.reply(f"لیست دشمنان:\n{users}")
    else:
        await message.reply("هیچ دشمنی وجود ندارد.")

@app.on_message(filters.command("clearenemylist"))
async def clear_enemy_list(client, message: Message):
    enemies.clear()
    await message.reply("لیست دشمنان پاک شد.")

@app.on_message(filters.command("enemytext") & filters.reply)
async def add_enemy_text(client, message: Message):
    text = message.reply_to_message.text
    if text:
        enemy_texts.append(text)
        await message.reply("متن به لیست دشمنان اضافه شد.")
    else:
        await message.reply("لطفاً روی یک پیام متنی ریپلای کنید.")

@app.on_message(filters.command("resetenemytext"))
async def reset_enemy_text(client, message: Message):
    global enemy_texts
    enemy_texts = default_enemy_texts.copy()
    await message.reply("لیست متن‌های دشمن به حالت اولیه بازگردانی شد.")

# Love commands
@app.on_message(filters.command("setlove") & filters.reply)
async def set_love(client, message: Message):
    user_id = message.reply_to_message.from_user.id
    loves.add(user_id)
    await message.reply("کاربر به لیست دوستان اضافه شد.")

@app.on_message(filters.command("dellove") & filters.reply)
async def del_love(client, message: Message):
    user_id = message.reply_to_message.from_user.id
    loves.discard(user_id)
    await message.reply("کاربر از لیست دوستان خارج شد.")

@app.on_message(filters.command("lovelist"))
async def love_list(client, message: Message):
    if loves:
        users = "\n".join([str(user_id) for user_id in loves])
        await message.reply(f"لیست دوستان:\n{users}")
    else:
        await message.reply("هیچ دوستی وجود ندارد.")

@app.on_message(filters.command("clearlovelist"))
async def clear_love_list(client, message: Message):
    loves.clear()
    await message.reply("لیست دوستان پاک شد.")

@app.on_message(filters.command("lovetext") & filters.reply)
async def add_love_text(client, message: Message):
    text = message.reply_to_message.text
    if text:
        love_texts.append(text)
        await message.reply("متن به لیست دوستان اضافه شد.")
    else:
        await message.reply("لطفاً روی یک پیام متنی ریپلای کنید.")

@app.on_message(filters.command("resetlovetext"))
async def reset_love_text(client, message: Message):
    global love_texts
    love_texts = default_love_texts.copy()
    await message.reply("لیست متن‌های دوستان به حالت اولیه بازگردانی شد.")

# Block commands
@app.on_message(filters.command("block") & filters.reply)
async def block_user(client, message: Message):
    user_id = message.reply_to_message.from_user.id
    await app.block_user(user_id)
    await message.reply("کاربر مسدود شد.")

@app.on_message(filters.command("unblock") & filters.reply)
async def unblock_user(client, message: Message):
    user_id = message.reply_to_message.from_user.id
    await app.unblock_user(user_id)
    await message.reply("کاربر از حالت مسدودی خارج شد.")

# Timename commands
@app.on_message(filters.command("timename"))
async def timename(client, message: Message):
    global timename_enabled
    args = message.command[1] if len(message.command) > 1 else ""
    if args.lower() == "on":
        timename_enabled = True
        await message.reply("قابلیت ساعت در نام فعال شد.")
        asyncio.create_task(update_timename())
    elif args.lower() == "off":
        timename_enabled = False
        await app.update_profile(last_name="")
        await message.reply("قابلیت ساعت در نام غیرفعال شد.")
    else:
        await message.reply("لطفاً on یا off را مشخص کنید.")

@app.on_message(filters.command("setfont"))
async def set_font(client, message: Message):
    global current_font
    args = message.command[1] if len(message.command) > 1 else ""
    if args in fonts or args == "random":
        current_font = args
        await message.reply(f"فونت به {args} تغییر کرد.")
    else:
        await message.reply("فونت نامعتبر! لطفاً یکی از فونت‌های 1 تا 13 یا random را انتخاب کنید.")

# Timebio commands
@app.on_message(filters.command("timebio1"))
async def timebio1(client, message: Message):
    global timebio1_enabled
    args = message.command[1] if len(message.command) > 1 else ""
    if args.lower() == "on":
        timebio1_enabled = True
        await message.reply("قابلیت timebio1 فعال شد.")
        asyncio.create_task(update_timebio())
    elif args.lower() == "off":
        timebio1_enabled = False
        await message.reply("قابلیت timebio1 غیرفعال شد.")
    else:
        await message.reply("لطفاً on یا off را مشخص کنید.")

@app.on_message(filters.command("timebio2"))
async def timebio2(client, message: Message):
    global timebio2_enabled
    args = message.command[1] if len(message.command) > 1 else ""
    if args.lower() == "on":
        timebio2_enabled = True
        await message.reply("قابلیت timebio2 فعال شد.")
        asyncio.create_task(update_timebio())
    elif args.lower() == "off":
        timebio2_enabled = False
        await message.reply("قابلیت timebio2 غیرفعال شد.")
    else:
        await message.reply("لطفاً on یا off را مشخص کنید.")

# Antilogin
@app.on_message(filters.command("antilogin"))
async def antilogin(client, message: Message):
    global antilogin_enabled
    args = message.command[1] if len(message.command) > 1 else ""
    if args.lower() == "on":
        antilogin_enabled = True
        await message.reply("قابلیت آنتی‌لاگین فعال شد.")
    elif args.lower() == "off":
        antilogin_enabled = False
        await message.reply("قابلیت آنتی‌لاگین غیرفعال شد.")
    else:
        await message.reply("لطفاً on یا off را مشخص کنید.")

# Text mode commands
@app.on_message(filters.command(["bold", "spoiler", "italic", "code", "underline", "strike", "quote", "montion"]))
async def set_text_mode(client, message: Message):
    mode = message.command[0]
    args = message.command[1] if len(message.command) > 1 else ""
    if args.lower() == "on":
        text_modes[mode] = True
        await message.reply(f"حالت {mode} فعال شد.")
    elif args.lower() == "off":
        text_modes[mode] = False
        await message.reply(f"حالت {mode} غیرفعال شد.")
    else:
        await message.reply("لطفاً on یا off را مشخص کنید.")

# Handle sent messages for text modes
@app.on_message(filters.me & ~filters.command([""]))
async def handle_text_modes(client, message: Message):
    if not message.text:
        return
    entities = []
    if text_modes["bold"]:
        entities.append({"type": "bold", "offset": 0, "length": len(message.text)})
    if text_modes["spoiler"]:
        entities.append({"type": "spoiler", "offset": 0, "length": len(message.text)})
    if text_modes["italic"]:
        entities.append({"type": "italic", "offset": 0, "length": len(message.text)})
    if text_modes["code"]:
        entities.append({"type": "code", "offset": 0, "length": len(message.text)})
    if text_modes["underline"]:
        entities.append({"type": "underline", "offset": 0, "length": len(message.text)})
    if text_modes["strike"]:
        entities.append({"type": "strikethrough", "offset": 0, "length": len(message.text)})
    if text_modes["quote"]:
        entities.append({"type": "blockquote", "offset": 0, "length": len(message.text)})
    if text_modes["montion"]:
        user = await app.get_me()
        entities.append({"type": "text_mention", "offset": 0, "length": len(message.text), "user": user})
    
    if entities:
        await message.edit(message.text, entities=entities)

# Cheating commands
@app.on_message(filters.command("tas"))
async def tas_cheat(client, message: Message):
    target = int(message.command[1]) if len(message.command) > 1 and message.command[1].isdigit() else None
    if not target or target < 1 or target > 6:
        await message.reply("لطفاً یک عدد بین 1 تا 6 وارد کنید.")
        return
    dice = await app.send_dice(message.chat.id, emoji="🎲")
    while dice.dice.value != target:
        await dice.delete()
        dice = await app.send_dice(message.chat.id, emoji="🎲")

@app.on_message(filters.command("dart"))
async def dart_cheat(client, message: Message):
    dart = await app.send_dice(message.chat.id, emoji="🎯")
    while dart.dice.value != 6:
        await dart.delete()
        dart = await app.send_dice(message.chat.id, emoji="🎯")

@app.on_message(filters.command("bowling"))
async def bowling_cheat(client, message: Message):
    bowling = await app.send_dice(message.chat.id, emoji="🎳")
    while bowling.dice.value != 6:
        await bowling.delete()
        bowling = await app.send_dice(message.chat.id, emoji="🎳")

@app.on_message(filters.command("basketball"))
async def basketball_cheat(client, message: Message):
    basketball = await app.send_dice(message.chat.id, emoji="🏀")
    while basketball.dice.value != 5:
        await basketball.delete()
        basketball = await app.send_dice(message.chat.id, emoji="🏀")

@app.on_message(filters.command("football"))
async def football_cheat(client, message: Message):
    args = message.command[1] if len(message.command) > 1 else ""
    target = 5 if args.upper() == "G" else 3
    football = await app.send_dice(message.chat.id, emoji="⚽")
    while football.dice.value != target:
        await football.delete()
        football = await app.send_dice(message.chat.id, emoji="⚽")

# AI command
@app.on_message(filters.command("GPT4"))
async def gpt4(client, message: Message):
    text = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    if not text:
        await message.reply("لطفاً یک متن وارد کنید.")
        return
    url = f"https://api.fast-creat.ir/gpt/chat?apikey=8497435557:Lkh2j05U8pc7fnv@Api_ManagerRoBot&text={text}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("ok"):
            result_text = data["result"]["text"]
            await message.reply(f"✅ جواب دریافت شد:\n{result_text}")
        else:
            await message.reply("خطا در دریافت پاسخ از API.")
    else:
        await message.reply("خطا در اتصال به API.")

# Translation commands
@app.on_message(filters.command("transen"))
async def translate_to_en(client, message: Message):
    text = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    if not text:
        await message.reply("لطفاً یک متن وارد کنید.")
        return
    url = f"https://api.fast-creat.ir/translate?apikey=8497435557:KwnPuvTI8gj15tb@Api_ManagerRoBot&text={text}&to=en"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("ok"):
            translated = data["result"]["translate"]
            await message.reply(f"✅ ترجمه انجام شد:\n{text}\n——————————\n{translated}")
        else:
            await message.reply("خطا در دریافت پاسخ از API.")
    else:
        await message.reply("خطا در اتصال به API.")

@app.on_message(filters.command("transfa"))
async def translate_to_fa(client, message: Message):
    text = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    if not text:
        await message.reply("لطفاً یک متن وارد کنید.")
        return
    url = f"https://api.fast-creat.ir/translate?apikey=8497435557:KwnPuvTI8gj15tb@Api_ManagerRoBot&text={text}&to=fa"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("ok"):
            translated = data["result"]["translate"]
            await message.reply(f"✅ ترجمه انجام شد:\n{text}\n——————————\n{translated}")
        else:
            await message.reply("خطا در دریافت پاسخ از API.")
    else:
        await message.reply("خطا در اتصال به API.")

# Handle muted users and enemy/love responses
@app.on_message(filters.private)
async def handle_private_messages(client, message: Message):
    user_id = message.from_user.id
    if user_id in muted_users:
        await message.delete()
    elif user_id in enemies:
        await message.reply(random.choice(enemy_texts))
    elif user_id in loves:
        await message.reply(random.choice(love_texts))

# Handle antilogin
@app.on_message(filters.service & filters.regex(r"Your login code"))
async def handle_login_code(client, message: Message):
    if antilogin_enabled:
        await message.forward("me")
        await message.delete()

async def main():
    await app.start()
    print("Bot is running...")
    await asyncio.Event().wait()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
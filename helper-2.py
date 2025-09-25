import json
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent, CallbackQuery, InlineQuery

# تنظیمات اولیه (جایگزین کن)
bot_token = "8443732335:AAFD3JQtsWR-ulBhPi5RIF2yhuYb6VBKzKk"  # از @BotFather

# تابع لود و سیو
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

app = Client("helperbot", bot_token=bot_token)

# تابع برای ساخت کیبورد
def get_panel_keyboard(settings):
    check = "✔️"
    cross = "✖️"
    buttons = [
        [InlineKeyboardButton(f"منشی ({check if settings['secretary_on'] else cross})", callback_data="toggle_secretary")],
        [InlineKeyboardButton(f"ساعت در نام ({check if settings['clock_on'] else cross})", callback_data="toggle_clock")],
        [InlineKeyboardButton(f"حالت بولد ({check if settings['bold_mode'] else cross})", callback_data="toggle_bold")],
        [InlineKeyboardButton(f"فونت normal ({check if settings['clock_font'] == 'normal' else cross})", callback_data="font_normal")],
        [InlineKeyboardButton(f"فونت bold ({check if settings['clock_font'] == 'bold' else cross})", callback_data="font_bold")],
        [InlineKeyboardButton(f"فونت circle ({check if settings['clock_font'] == 'circle' else cross})", callback_data="font_circle")],
        [InlineKeyboardButton(f"فونت random ({check if settings['clock_font'] == 'random' else cross})", callback_data="font_random")]
    ]
    return InlineKeyboardMarkup(buttons)

# هندلر برای inline query
@app.on_inline_query(filters.regex(r"^panel$"))
async def inline_panel(client, inline_query: InlineQuery):
    settings = load_settings()
    keyboard = get_panel_keyboard(settings)
    results = [
        InlineQueryResultArticle(
            id="panel",
            title="پنل مدیریت",
            input_message_content=InputTextMessageContent("پنل مدیریت:"),
            reply_markup=keyboard
        )
    ]
    await inline_query.answer(results, is_personal=True)

# هندلر برای کال‌بک (toggle و فونت‌ها)
@app.on_callback_query()
async def callback_handler(client, query: CallbackQuery):
    data = query.data
    settings = load_settings()
    if data == "toggle_secretary":
        settings["secretary_on"] = not settings["secretary_on"]
    elif data == "toggle_clock":
        settings["clock_on"] = not settings["clock_on"]
    elif data == "toggle_bold":
        settings["bold_mode"] = not settings["bold_mode"]
    elif data.startswith("font_"):
        font = data.split("_")[1]
        settings["clock_font"] = font
    save_settings(settings)
    new_keyboard = get_panel_keyboard(settings)
    await query.edit_message_reply_markup(reply_markup=new_keyboard)
    await query.answer("تغییر اعمال شد!")

app.run()
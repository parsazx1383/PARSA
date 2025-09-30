# helper.py - Helper Bot for Inline Panel

from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
import json

bot_token = "7594037635:AAHKEUsqUauws8TQ2BGrwRFrqROf2BZKPCk"  # Replace with actual bot token
api_id = 28285817
api_hash = "5c96b16dea2daf25995ef30a02424bb9"
app = Client("helper", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

STATE_FILE = 'states.json'  # Shared with self-bot

def load_states():
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_states(states):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(states, f, ensure_ascii=False)

# List of all toggle modes for easy checking
text_modes = ['bold', 'spoiler', 'italic', 'code', 'underline', 'strike', 'quote', 'montion']
action_modes_list = ['typing', 'gaming', 'uphoto', 'uvideo', 'uvoice', 'umusic', 'ufile', 'csticker']
timebio_modes = ['timebio1', 'timebio2']
lock_modes = ['lphoto', 'lvideo', 'lmessage', 'lsticker', 'lgif', 'lemoji', 'lcontact', 'lvoice', 'lmusic', 'lfile', 'lockpv']
single_toggles = {
    'timename': 'ساعت در نام',
    'antilogin': 'آنتی لاگین',
    'savetime': 'ذخیره تایمردار',
    'pmenemy': 'حذف پیام دشمن',
    'monshi': 'منشی',
    'command': 'کامنت اول',
    'autoseen': 'سین خودکار',
}

# Sections
sections = {
    "main": [
        ["• حالت سکوت •"],
        ["• دشمن •", "• دوست •"],
        ["• بلاک •"],
        ["• ساعت در نام •", "• ساعت در بیو •"],
        ["• آنتی لاگین •"],
        ["• حالت متن •", "• حالت اکشن •"],
        ["• تقلب •"],
        ["• هوش مصنوعی •", "• ترجمه متن •"],
        ["• نرخ ارز •"],
        ["• دانلود محتوای قفل شده •", "• تنظیم متن •"],
        ["• امضا •"],
        ["• ذخیره تایمردار •", "• حذف پیام دشمن •"],
        ["• قفل پیوی •"],
        ["• منشی •", "• کامنت اول •"],
        ["• سین خودکار •"],
        ["• فیلتر کلمه •", "• اسپم •"],
    ],
    "حالت متن": [  # text_modes
        [f"ایتالیک ({'✔️' if load_states().get('italic', 'off') == 'on' else '✖️'})", "callback:italic"],
        [f"بولد ({'✔️' if load_states().get('bold', 'off') == 'on' else '✖️'})", "callback:bold"],
        [f"زیرخط ({'✔️' if load_states().get('underline', 'off') == 'on' else '✖️'})", "callback:underline"],
        [f"خط‌خورده ({'✔️' if load_states().get('strike', 'off') == 'on' else '✖️'})", "callback:strike"],
        [f"اسپویلر ({'✔️' if load_states().get('spoiler', 'off') == 'on' else '✖️'})", "callback:spoiler"],
        [f"کد ({'✔️' if load_states().get('code', 'off') == 'on' else '✖️'})", "callback:code"],
        [f"نقل قول ({'✔️' if load_states().get('quote', 'off') == 'on' else '✖️'})", "callback:quote"],
        [f"منشن ({'✔️' if load_states().get('montion', 'off') == 'on' else '✖️'})", "callback:montion"],
    ],
    "حالت اکشن": [  # action_modes
        [f"تایپینگ ({'✔️' if load_states().get('typing', 'off') == 'on' else '✖️'})", "callback:typing"],
        [f"گیمینگ ({'✔️' if load_states().get('gaming', 'off') == 'on' else '✖️'})", "callback:gaming"],
        [f"آپ عکس ({'✔️' if load_states().get('uphoto', 'off') == 'on' else '✖️'})", "callback:uphoto"],
        [f"آپ ویدیو ({'✔️' if load_states().get('uvideo', 'off') == 'on' else '✖️'})", "callback:uvideo"],
        [f"ویس ({'✔️' if load_states().get('uvoice', 'off') == 'on' else '✖️'})", "callback:uvoice"],
        [f"موزیک ({'✔️' if load_states().get('umusic', 'off') == 'on' else '✖️'})", "callback:umusic"],
        [f"فایل ({'✔️' if load_states().get('ufile', 'off') == 'on' else '✖️'})", "callback:ufile"],
        [f"استیکر ({'✔️' if load_states().get('csticker', 'off') == 'on' else '✖️'})", "callback:csticker"],
    ],
    "ساعت در بیو": [  # timebio
        [f"بیو 1 ({'✔️' if load_states().get('timebio1', 'off') == 'on' else '✖️'})", "callback:timebio1"],
        [f"بیو 2 ({'✔️' if load_states().get('timebio2', 'off') == 'on' else '✖️'})", "callback:timebio2"],
    ],
    "قفل پیوی": [  # lockpv
        [f"عکس ({'✔️' if load_states().get('lphoto', 'off') == 'on' else '✖️'})", "callback:lphoto"],
        [f"ویدیو ({'✔️' if load_states().get('lvideo', 'off') == 'on' else '✖️'})", "callback:lvideo"],
        [f"پیام ({'✔️' if load_states().get('lmessage', 'off') == 'on' else '✖️'})", "callback:lmessage"],
        [f"استیکر ({'✔️' if load_states().get('lsticker', 'off') == 'on' else '✖️'})", "callback:lsticker"],
        [f"گیف ({'✔️' if load_states().get('lgif', 'off') == 'on' else '✖️'})", "callback:lgif"],
        [f"ایموجی ({'✔️' if load_states().get('lemoji', 'off') == 'on' else '✖️'})", "callback:lemoji"],
        [f"مخاطب ({'✔️' if load_states().get('lcontact', 'off') == 'on' else '✖️'})", "callback:lcontact"],
        [f"ویس ({'✔️' if load_states().get('lvoice', 'off') == 'on' else '✖️'})", "callback:lvoice"],
        [f"موزیک ({'✔️' if load_states().get('lmusic', 'off') == 'on' else '✖️'})", "callback:lmusic"],
        [f"فایل ({'✔️' if load_states().get('lfile', 'off') == 'on' else '✖️'})", "callback:lfile"],
        [f"قفل کامل ({'✔️' if load_states().get('lockpv', 'off') == 'on' else '✖️'})", "callback:lockpv"],
    ],
    "ساعت در نام": [  # timename as single toggle
        [f"ساعت در نام ({'✔️' if load_states().get('timename', 'off') == 'on' else '✖️'})", "callback:timename"],
    ],
    "آنتی لاگین": [
        [f"آنتی لاگین ({'✔️' if load_states().get('antilogin', 'off') == 'on' else '✖️'})", "callback:antilogin"],
    ],
    "ذخیره تایمردار": [
        [f"ذخیره تایمردار ({'✔️' if load_states().get('savetime', 'off') == 'on' else '✖️'})", "callback:savetime"],
    ],
    "حذف پیام دشمن": [
        [f"حذف پیام دشمن ({'✔️' if load_states().get('pmenemy', 'off') == 'on' else '✖️'})", "callback:pmenemy"],
    ],
    "منشی": [
        [f"منشی ({'✔️' if load_states().get('monshi', 'off') == 'on' else '✖️'})", "callback:monshi"],
    ],
    "کامنت اول": [
        [f"کامنت اول ({'✔️' if load_states().get('command', 'off') == 'on' else '✖️'})", "callback:command"],
    ],
    "سین خودکار": [
        [f"سین خودکار ({'✔️' if load_states().get('autoseen', 'off') == 'on' else '✖️'})", "callback:autoseen"],
    ],
    # For non-toggle sections, empty list, will show welcome text and back/channel buttons
    "حالت سکوت": [],
    "دشمن": [],
    "دوست": [],
    "بلاک": [],
    "تقلب": [],
    "هوش مصنوعی": [],
    "ترجمه متن": [],
    "نرخ ارز": [],
    "دانلود محتوای قفل شده": [],
    "تنظیم متن": [],
    "امضا": [],
    "فیلتر کلمه": [],
    "اسپم": [],
}

channel_button = InlineKeyboardButton("کانال ما", url="https://t.me/yourchannel")  # Replace with your channel URL

def get_section_text(section):
    # Custom welcome texts for sections
    default = f"**به بخش {section} خوش آمدید.**"
    non_toggle_texts = {
        "حالت سکوت": "**به بخش حالت سکوت خوش آمدید.**\nدستورات: .mute, .unmute, .mutelist, .clearmutelist",
        "دشمن": "**به بخش دشمن خوش آمدید.**\nدستورات: .setenemy, .delenemy, .enemylist, .clearenemylist, .emenytext, .resetenemytext",
        "دوست": "**به بخش دوست خوش آمدید.**\nدستورات: .setlove, .dellove, .lovelist, .clearlovelist, .lovetext, .resetlovetext",
        "بلاک": "**به بخش بلاک خوش آمدید.**\nدستورات: .block, .unblock",
        "تقلب": "**به بخش تقلب خوش آمدید.**\nدستورات: .tas, .dart, .bowling, .basketball, .football",
        "هوش مصنوعی": "**به بخش هوش مصنوعی خوش آمدید.**\nدستور: .GPT4",
        "ترجمه متن": "**به بخش ترجمه متن خوش آمدید.**\nدستورات: .transen, .transfa",
        "نرخ ارز": "**به بخش نرخ ارز خوش آمدید.**\nدستورات: .crypto, .arz",
        "دانلود محتوای قفل شده": "**به بخش دانلود محتوای قفل شده خوش آمدید.**\nدستور: .plink",
        "تنظیم متن": "**به بخش تنظیم متن خوش آمدید.**\nدستور: .setnm",
        "امضا": "**به بخش امضا خوش آمدید.**\nدستورات: .setsign, .delsign",
        "فیلتر کلمه": "**به بخش فیلتر کلمه خوش آمدید.**\nدستورات: .pmfilter, .delpmfilter, .filterslist",
        "اسپم": "**به بخش اسپم خوش آمدید.**\nدستورات: .fastspam, .slowspam",
    }
    return non_toggle_texts.get(section, default)

def build_markup(section, page=0):
    states = load_states()  # Reload states for updated status
    buttons = []
    sec_buttons = sections.get(section, [])
    # Update button texts with current status
    updated_buttons = []
    for btn in sec_buttons:
        if len(btn) == 2:
            text, data = btn
            mode = data.split(':')[1] if 'callback:' in data else None
            if mode:
                status = '✔️' if states.get(mode, 'off') == 'on' else '✖️'
                text = text.replace('✔️', status).replace('✖️', status)  # Update if needed
            updated_buttons.append([text, data])
        else:
            updated_buttons.append(btn)
    per_page = 12
    start = page * per_page
    end = start + per_page
    paginated = updated_buttons[start:end]
    # Build rows as per paginated
    for item in paginated:
        if isinstance(item, list) and len(item) == 2:
            text, data = item
            buttons.append([InlineKeyboardButton(text, callback_data=data)])
        elif isinstance(item, list):
            row = []
            for sub in item:
                if isinstance(sub, list):
                    text, data = sub
                    row.append(InlineKeyboardButton(text, callback_data=data))
                else:
                    row.append(InlineKeyboardButton(sub, callback_data=f"section:{sub.strip(' •')}"))
            buttons.append(row)
        else:
            buttons.append([InlineKeyboardButton(item, callback_data=f"section:{item.strip(' •')}")])
    # Footer
    footer = [InlineKeyboardButton("برگشت", callback_data=f"back:main" if section != "main" else "close")]  # Assume close for main if needed
    if len(updated_buttons) > end:
        footer.insert(1, InlineKeyboardButton("بعدی", callback_data=f"page:{section}:{page+1}"))
    else:
        footer.append(channel_button)
    buttons.append(footer)
    return InlineKeyboardMarkup(buttons)

@app.on_inline_query()
async def inline_query(_, query):
    if query.query == "panel":
        markup = build_markup("main")
        result = InlineQueryResultArticle(
            title="پنل راهنما",
            input_message_content=InputTextMessageContent("**به پنل راهنمای سلف ویژه خوش آمدید.**\n**لطفا انتخاب کنید :**", parse_mode=enums.ParseMode.MARKDOWN),
            reply_markup=markup
        )
        await query.answer([result])

@app.on_callback_query()
async def callback_query(_, cb):
    data = cb.data
    states = load_states()
    if data.startswith("callback:"):
        mode = data.split(":")[1]
        current = states.get(mode, 'off')
        states[mode] = 'off' if current == 'on' else 'on'
        save_states(states)
        # Determine section based on mode
        if mode in text_modes:
            section = "حالت متن"
        elif mode in action_modes_list:
            section = "حالت اکشن"
        elif mode in timebio_modes:
            section = "ساعت در بیو"
        elif mode in lock_modes:
            section = "قفل پیوی"
        elif mode in single_toggles:
            section = single_toggles[mode]
        else:
            section = "main"
        new_markup = build_markup(section)
        await cb.edit_message_reply_markup(new_markup)
        await cb.answer(f"حالت {mode} به {states[mode]} تغییر یافت.")
    elif data.startswith("section:"):
        section = data.split(":")[1]
        new_markup = build_markup(section)
        section_text = get_section_text(section)
        await cb.edit_message_text(section_text, parse_mode=enums.ParseMode.MARKDOWN)
        await cb.edit_message_reply_markup(new_markup)
    elif data.startswith("back:"):
        back_sec = data.split(":")[1]
        new_markup = build_markup(back_sec)
        text = "**به پنل راهنمای سلف ویژه خوش آمدید.**\n**لطفا انتخاب کنید :**" if back_sec == "main" else get_section_text(back_sec)
        await cb.edit_message_text(text, parse_mode=enums.ParseMode.MARKDOWN)
        await cb.edit_message_reply_markup(new_markup)
    elif data.startswith("page:"):
        parts = data.split(":")
        section = parts[1]
        pg = int(parts[2])
        new_markup = build_markup(section, pg)
        await cb.edit_message_reply_markup(new_markup)
    elif data == "close":
        await cb.edit_message_text("**پنل بسته شد.**")

app.run(), print("runned")
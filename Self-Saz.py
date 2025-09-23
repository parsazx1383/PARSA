# First, install required libraries if not already installed:
# pip install pyrogram tgcrypto sqlite3 schedule subprocess asyncio

import os
import sqlite3
import time
import threading
import subprocess
import asyncio
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import SessionPasswordNeeded

# Bot configuration
API_ID = 28285817  # Replace with your API ID
API_HASH = "5c96b16dea2daf25995ef30a02424bb9"  # Replace with your API Hash
BOT_TOKEN = "8443732335:AAFD3JQtsWR-ulBhPi5RIF2yhuYb6VBKzKk"  # Replace with your bot token
ADMIN_ID = 8497435557  # Replace with admin Telegram ID (for support and payments)
CARD_NUMBER = "6037-7013-1079-3028"  # Replace with your card number for payments

# Database setup
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0,
    self_active BOOLEAN DEFAULT FALSE,
    self_process_id TEXT DEFAULT NULL,
    banned BOOLEAN DEFAULT FALSE,
    blocked BOOLEAN DEFAULT FALSE
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount INTEGER,
    photo_id TEXT,
    status TEXT DEFAULT 'pending'
)
''')
conn.commit()

# Bot client
bot = Client("self_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# User states for login
user_states = {}  # dict to hold user states: {'stage': str, 'phone': str, 'hash': str, 'code': str, 'app': Client}

# Function to deduct diamonds hourly
def deduct_diamonds():
    while True:
        cursor.execute("SELECT user_id FROM users WHERE self_active = TRUE")
        users = cursor.fetchall()
        for user in users:
            user_id = user[0]
            cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
            balance = cursor.fetchone()[0]
            if balance >= 2:
                new_balance = balance - 2
                cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
                conn.commit()
            else:
                # Turn off self
                cursor.execute("UPDATE users SET self_active = FALSE WHERE user_id = ?", (user_id,))
                conn.commit()
                # Kill the self process
                cursor.execute("SELECT self_process_id FROM users WHERE user_id = ?", (user_id,))
                proc_id = cursor.fetchone()[0]
                if proc_id:
                    try:
                        os.system(f"kill {proc_id}")
                    except:
                        pass
                cursor.execute("UPDATE users SET self_process_id = NULL WHERE user_id = ?", (user_id,))
                conn.commit()
                bot.send_message(user_id, "الماس شما تمام شد. سلف خاموش شد.")
        time.sleep(3600)  # Every hour

# Start deduction thread
threading.Thread(target=deduct_diamonds, daemon=True).start()

# Start command
@bot.on_message(filters.command("start") & filters.private)
def start(client, message):
    user_id = message.from_user.id
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("پنل کاربر", callback_data="user_panel")],
        [InlineKeyboardButton("پشتیبانی", callback_data="support")],
        [InlineKeyboardButton("افزایش موجودی", callback_data="increase_balance")]
    ])
    message.reply("خوش آمدید! لطفاً گزینه مورد نظر را انتخاب کنید.", reply_markup=keyboard)

# Callback handler
@bot.on_callback_query()
def callback(client, query):
    user_id = query.from_user.id
    data = query.data

    cursor.execute("SELECT banned, blocked FROM users WHERE user_id = ?", (user_id,))
    user_status = cursor.fetchone()
    if user_status and (user_status[0] or user_status[1]):
        query.answer("شما بن یا بلاک شده‌اید.", show_alert=True)
        return

    if data == "user_panel":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("فعال کردن سلف", callback_data="activate_self")],
            [InlineKeyboardButton("خاموش کردن سلف", callback_data="deactivate_self")],
            [InlineKeyboardButton("موجودی", callback_data="balance")],
            [InlineKeyboardButton("نرخ‌ها", callback_data="rates")],
            [InlineKeyboardButton("بازگشت", callback_data="back")]
        ])
        query.message.edit_text("پنل کاربر:", reply_markup=keyboard)

    elif data == "support":
        query.message.edit_text("لطفاً پیام خود را ارسال کنید.")

    elif data == "increase_balance":
        query.message.edit_text(f"شماره کارت: {CARD_NUMBER}\nلطفاً فیش پرداخت را به صورت عکس ارسال کنید.")

    elif data == "activate_self":
        cursor.execute("SELECT balance, self_active FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()
        if user_data[1]:
            query.answer("سلف قبلاً فعال است.", show_alert=True)
            return
        if user_data[0] < 31:
            query.answer("موجودی کافی برای لاگین نیست (31 الماس).", show_alert=True)
            return
        # Deduct login cost
        new_balance = user_data[0] - 31
        cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
        conn.commit()
        # Start login process
        bot.send_message(user_id, "لطفاً شماره تلفن خود را با فرمت +989xxxxxxxxx ارسال کنید.")
        user_states[user_id] = {'stage': 'phone'}

    elif data == "deactivate_self":
        cursor.execute("UPDATE users SET self_active = FALSE WHERE user_id = ?", (user_id,))
        conn.commit()
        cursor.execute("SELECT self_process_id FROM users WHERE user_id = ?", (user_id,))
        proc_id = cursor.fetchone()[0]
        if proc_id:
            try:
                os.system(f"kill {proc_id}")
            except:
                pass
        cursor.execute("UPDATE users SET self_process_id = NULL WHERE user_id = ?", (user_id,))
        conn.commit()
        query.answer("سلف خاموش شد.", show_alert=True)

    elif data == "balance":
        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        balance = cursor.fetchone()[0]
        query.answer(f"موجودی شما: {balance} الماس", show_alert=True)

    elif data == "rates":
        query.message.edit_text("نرخ ماهانه: 1440 الماس\nهزینه لاگین: 31 الماس\nهر ساعت: 2 الماس")

    elif data == "back":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("پنل کاربر", callback_data="user_panel")],
            [InlineKeyboardButton("پشتیبانی", callback_data="support")],
            [InlineKeyboardButton("افزایش موجودی", callback_data="increase_balance")]
        ])
        query.message.edit_text("خوش آمدید! لطفاً گزینه مورد نظر را انتخاب کنید.", reply_markup=keyboard)

    elif data.startswith("code_"):
        if user_id not in user_states or user_states[user_id]['stage'] != 'code':
            return
        state = user_states[user_id]
        action = data[5:]
        if action.isdigit():
            state['code'] += action
        elif action == 'delete':
            if state['code']:
                state['code'] = state['code'][:-1]
        elif action == 'confirm':
            if len(state['code']) == 5:  # Assuming 5 digit code
                app = state['app']
                try:
                    app.sign_in(state['phone'], state['hash'], state['code'])
                    # Login successful
                    session_name = f"user_{user_id}"
                    run_self(user_id, session_name)
                    query.message.edit_text("لاگین موفق. سلف فعال شد.")
                    del user_states[user_id]
                except SessionPasswordNeeded:
                    state['stage'] = 'password'
                    query.message.edit_text("رمز دو مرحله‌ای مورد نیاز است. لطفاً رمز را ارسال کنید.")
                except Exception as e:
                    query.message.edit_text(f"خطا: {str(e)}")
                    del user_states[user_id]
            else:
                query.answer("کد کامل نیست.", show_alert=True)
                return
        send_code_keyboard(user_id, state['code'])

# Handle photo for payment
@bot.on_message(filters.photo & filters.private)
def handle_photo(client, message):
    user_id = message.from_user.id
    photo_id = message.photo.file_id
    message.reply("لطفاً مبلغ پرداخت شده را وارد کنید.")
    user_states[user_id] = {'stage': 'payment_amount', 'photo_id': photo_id}

# Handle text messages for login, payment, support
@bot.on_message(filters.text & filters.private)
def handle_text(client, message):
    user_id = message.from_user.id
    if user_id in user_states:
        state = user_states[user_id]
        if state['stage'] == 'phone':
            phone = message.text.strip()
            session_name = f"user_{user_id}"
            app = Client(session_name, api_id=API_ID, api_hash=API_HASH)
            try:
                code_request = app.send_code(phone)
                state['phone'] = phone
                state['hash'] = code_request.phone_code_hash
                state['code'] = ''
                state['stage'] = 'code'
                state['app'] = app
                send_code_keyboard(user_id, '')
                message.reply("کد تایید ارسال شد. لطفاً کد را با کیبورد زیر وارد کنید.")
            except Exception as e:
                message.reply(f"خطا: {str(e)}")
                del user_states[user_id]
        elif state['stage'] == 'code':
            # Code is handled via callback, so ignore text
            pass
        elif state['stage'] == 'password':
            password = message.text.strip()
            app = state['app']
            try:
                app.sign_in(state['phone'], state['hash'], state['code'], password=password)
                # Login successful
                session_name = f"user_{user_id}"
                run_self(user_id, session_name)
                message.reply("لاگین موفق. سلف فعال شد.")
                del user_states[user_id]
            except Exception as e:
                message.reply(f"خطا در رمز: {str(e)}")
        elif state['stage'] == 'payment_amount':
            try:
                amount = int(message.text)
                cursor.execute("INSERT INTO payments (user_id, amount, photo_id) VALUES (?, ?, ?)", (user_id, amount, state['photo_id']))
                conn.commit()
                message.reply("فیش ارسال شد. منتظر تایید مدیر باشید.")
                bot.send_photo(ADMIN_ID, state['photo_id'], caption=f"پرداخت جدید از {user_id}: {amount} الماس")
                # For confirmation, admin can use /confirm_payment id amount (manual for now since no admin panel)
            except:
                message.reply("مبلغ نامعتبر.")
            del user_states[user_id]
    else:
        # Support message
        bot.forward_messages(ADMIN_ID, message.chat.id, message.id)
        message.reply("پیام شما به پشتیبانی ارسال شد.")

# Function to send code keyboard
def send_code_keyboard(user_id, current_code):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("1", callback_data="code_1"), InlineKeyboardButton("2", callback_data="code_2"), InlineKeyboardButton("3", callback_data="code_3")],
        [InlineKeyboardButton("4", callback_data="code_4"), InlineKeyboardButton("5", callback_data="code_5"), InlineKeyboardButton("6", callback_data="code_6")],
        [InlineKeyboardButton("7", callback_data="code_7"), InlineKeyboardButton("8", callback_data="code_8"), InlineKeyboardButton("9", callback_data="code_9")],
        [InlineKeyboardButton("حذف آخرین", callback_data="code_delete"), InlineKeyboardButton("0", callback_data="code_0"), InlineKeyboardButton("تایید", callback_data="code_confirm")]
    ])
    bot.send_message(user_id, f"کد فعلی: {current_code or 'هیچ'}", reply_markup=keyboard)

# Function to run self
def run_self(user_id, session_name):
    proc = subprocess.Popen(["python", "Self-Bot.py", session_name])
    cursor.execute("UPDATE users SET self_active = TRUE, self_process_id = ? WHERE user_id = ?", (proc.pid, user_id))
    conn.commit()

# Admin command for confirming payments (since no panel, manual)
@bot.on_message(filters.command("confirm_payment") & filters.private)
def confirm_payment(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        parts = message.text.split()[1:]
        payment_id = int(parts[0])
        cursor.execute("SELECT user_id, amount FROM payments WHERE id = ? AND status = 'pending'", (payment_id,))
        payment = cursor.fetchone()
        if payment:
            user_id, amount = payment
            cursor.execute("UPDATE payments SET status = 'confirmed' WHERE id = ?", (payment_id,))
            cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
            conn.commit()
            bot.send_message(user_id, f"پرداخت شما تایید شد. {amount} الماس اضافه شد.")
            message.reply("تایید شد.")
    except:
        message.reply("خطا. فرمت: /confirm_payment id")

bot.run()
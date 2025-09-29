# self.py - Main Self-Bot Code using Pyrogram

from pyrogram import Client, filters, enums
from pyrogram.types import MessageEntity
from pyrogram.enums import ChatAction
import asyncio
import json
import time
import random
import requests
import os
from datetime import datetime
import re

# Client Setup
api_id = 12429393  # Replace with your actual api_id
api_hash = '2ec066334fb39f42e4ee8fbc5b640384'  # Replace with your actual api_hash
session_name = 'VIP-TG'
device_model = "iPhone 8 Plus"
system_version = "IOS-16.7.10"
app_version = "IOS 16.7.10"
lang_code = "en"

app = Client(session_name, api_id, api_hash, device_model=device_model, system_version=system_version, app_version=app_version, lang_code=lang_code)

# Main execution
async def main():
    await app.start()
    await on_startup()
    await app.idle()

if __name__ == "__main__":
    asyncio.run(main())
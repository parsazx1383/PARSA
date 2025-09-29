from pyrogram import Client
import asyncio

async def main():
    app = Client(
        "VIP-TG",
        api_id="12429393",
        api_hash="2ec066334fb39f42e4ee8fbc5b640384",
        device_model ="iPhone 8 Plus",
        system_version ="IOS-16.7.10",
        app_version ="IOS 16.7.10",
        lang_code ="en"
    )
    await app.start()
    print("Session created successfully!")
    await app.stop()

asyncio.run(main())
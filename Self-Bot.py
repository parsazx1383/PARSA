# self_bot.py - Separate self-bot code
# Run with: python self_bot.py session_name

import sys
import time
import asyncio
from pyrogram import Client

session_name = sys.argv[1]  # Get session_name from args

# Different font styles for numbers (Unicode characters)
FONTS = [
    {  # Normal
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', ':': ':'
    },
    {  # Bold Math
        '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒',
        '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗', ':': ':'
    },
    {  # Italic Math
        '0': '𝟢', '1': '𝟣', '2': '𝟤', '3': '𝟥', '4': '𝟦',
        '5': '𝟧', '6': '𝟨', '7': '𝟩', '8': '𝟪', '9': '𝟫', ':': ':'
    },
    {  # Monospace
        '0': '𝟶', '1': '𝟷', '2': '𝟸', '3': '𝟹', '4': '𝟺',
        '5': '𝟻', '6': '𝟼', '7': '𝟽', '8': '𝟾', '9': '𝟿', ':': ':'
    },
    {  # Circled
        '0': '⓪', '1': '①', '2': '②', '3': '③', '4': '④',
        '5': '⑤', '6': '⑥', '7': '⑦', '8': '⑧', '9': '⑨', ':': ':'
    },
    # Add more fonts if needed
]

async def main():
    app = Client(session_name)
    async with app:
        font_index = 0
        while True:
            current_time = time.strftime("%H:%M")
            font = FONTS[font_index % len(FONTS)]
            styled_time = ''.join(font.get(c, c) for c in current_time)
            await app.update_profile(first_name=f"Your Name {styled_time}")
            font_index += 1
            await asyncio.sleep(60)  # Update every minute

if __name__ == "__main__":
    asyncio.run(main())
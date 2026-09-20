import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# Environment variables se credentials uthayenge
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Pyrogram Bot Client initialize karein
app = Client(
    "RestrictedSaverBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    await message.reply_text(
        "👋 Hello!\n\n"
        "Main ek Restricted Content Saver Bot hoon.\n"
        "Mujhe kisi bhi restricted post ya media ka link bhejiye, main aapko file download karke de dunga!"
    )

@app.on_message(filters.text & ~filters.command(["start"]))
async def save_content(client, message: Message):
    text = message.text
    
    if "t.me/" in text:
        try:
            await message.reply_text("🔄 File fetch ho rahi hai, kripya intezaar karein...")
            
            parts = text.split("/")
            msg_id = int(parts[-1])
            
            if "c/" in text:
                chat_id = int("-100" + parts[-2])
            else:
                chat_id = parts[-2]

            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=chat_id,
                message_id=msg_id
            )
            
        except Exception as e:
            await message.reply_text(f"❌ Error aagya: {str(e)}\n\n(Dhyan rahe ki bot ya user us channel ka member hona chahiye jahan se link liya gaya hai.)")
    else:
        await message.reply_text("⚠️ Kripya ek valid Telegram post link bhejiye.")

# Naye method se event loop handle karne ke liye
if __name__ == "__main__":
    print("🤖 Bot started successfully...")
    app.run()
    

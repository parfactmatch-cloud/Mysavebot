import os
from telethon import TelegramClient, events

# Environment variables se credentials uthayenge
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Telethon Bot Client initialize karein
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
        "👋 Hello!\n\n"
        "Main ek Restricted Content Saver Bot hoon (Telethon powered).\n"
        "Mujhe kisi bhi restricted post ya media ka link bhejiye!"
    )

@client.on(events.NewMessage(pattern='t.me/'))
async def save_content(event):
    text = event.text
    try:
        await event.respond("🔄 File fetch ho rahi hai...")
        parts = text.split("/")
        msg_id = int(parts[-1])
        
        if "c/" in text:
            chat_id = int("-100" + parts[-2])
        else:
            chat_id = parts[-2]

        # Message forward/copy karna
        await client.send_message(event.chat_id, message=await client.get_messages(chat_id, ids=msg_id))
        
    except Exception as e:
        await event.respond(f"❌ Error aagya: {str(e)}")

print("🤖 Telethon Bot started successfully...")
client.run_until_disconnected()

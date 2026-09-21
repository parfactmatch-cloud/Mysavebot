import os
import asyncio
from aiohttp import web
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

# Web server Render ke liye
async def handle(request):
    return web.Response(text="Userbot is running!")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# Userbot Client
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Har jagah (Saved Messages ya kahin bhi) link detect karne ke liye
@client.on(events.NewMessage(outgoing=True))
async def grab_link(event):
    text = event.raw_text
    if text and "t.me/" in text and not text.startswith("/"):
        status = await event.reply("🔄 Link detect ho gaya, file fetch ho rahi hai...")
        try:
            parts = text.strip().split('/')
            msg_id = int(parts[-1])
            
            if "c/" in text:
                chat_id = int("-100" + parts[-2])
            else:
                chat_id = parts[-2]
                
            # Message fetch karein
            msg = await client.get_messages(chat_id, ids=msg_id)
            if msg and msg.media:
                file = await client.download_media(msg)
                await client.send_file(event.chat_id, file, caption=msg.text or "")
                if os.path.exists(file):
                    os.remove(file)
                await status.delete()
            else:
                await status.edit("❌ Is link par koi media file nahi mili.")
        except Exception as e:
            await status.edit(f"❌ Error: {str(e)}")

async def main():
    await web_server()
    await client.start()
    print("🤖 Userbot connected successfully...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
    

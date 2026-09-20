import os
from aiohttp import web
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Environment variables
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

# Dummy HTTP server (Render port scan pass karne ke liye)
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

# Userbot initialize karein StringSession ke sath
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("👋 Hello! Aapka Userbot active hai aur restricted content fetch kar sakta hai.")

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

        # Restricted content fetch karke user ko bhejna
        message = await client.get_messages(chat_id, ids=msg_id)
        await client.send_message(event.chat_id, message)
        
    except Exception as e:
        await event.respond(f"❌ Error aagya: {str(e)}")

async def main():
    await web_server()
    await client.start()
    print("🤖 Userbot started successfully...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    

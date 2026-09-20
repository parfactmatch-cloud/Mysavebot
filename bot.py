import os
from aiohttp import web
from telethon import TelegramClient, events

# Environment variables se credentials uthayenge
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Dummy HTTP server (Render ke port scan ko satisfy karne ke liye)
async def handle(request):
    return web.Response(text="Bot is running!")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# Telethon Bot Client initialize karein
client = TelegramClient('bot', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
        "👋 Hello!\n\n"
        "Main ek Restricted Content Saver Bot hoon.\n"
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

        await client.send_message(event.chat_id, message=await client.get_messages(chat_id, ids=msg_id))
        
    except Exception as e:
        await event.respond(f"❌ Error aagya: {str(e)}")

async def main():
    # Web server aur Telegram bot dono ek sath chalayenge
    await web_server()
    await client.start(bot_token=BOT_TOKEN)
    print("🤖 Bot and Web Server started successfully...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    

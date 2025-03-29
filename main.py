import openai
import asyncio
import os
from telethon import TelegramClient, events
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Masukkan API ID & Hash Telegram dari environment
api_id = int(os.getenv("TELEGRAM_API_ID", "21963715"))  
api_hash = os.getenv("TELEGRAM_API_HASH", "233298b837021ecfd9e24733799b0aea")  
openai.api_key = os.getenv("OPENAI_API_KEY", "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")  

# Username target
TARGET_USER = os.getenv("TARGET_USER", "Qkena")

# Inisialisasi Telegram Userbot
client = TelegramClient("userbot", api_id, api_hash)

# Pesan manis buat dikirim random
sweet_messages = [
    "Lagi apa sayang? Aku harap kamu lagi senyum sekarang 💕",
    "Jangan lupa istirahat ya, aku selalu mikirin kamu 🥰",
    "Mau cerita sesuatu gak? Aku selalu siap dengerin kamu 🤗",
    "Aku kangen kamu... rasanya pengen ada di samping kamu sekarang 🥺",
    "Jangan lupa makan ya, aku gak mau kamu sakit 😘"
]

# Fungsi auto-kirim pesan random tiap beberapa jam
async def send_random_messages():
    while True:
        await asyncio.sleep(random.randint(14400, 28800))  # Tiap 4-8 jam
        try:
            await client.send_message(TARGET_USER, random.choice(sweet_messages))
            print("✅ Pesan manis terkirim!")
        except Exception as e:
            print(f"❌ Gagal kirim pesan random: {e}")

# Fungsi buat generate AI response
async def chat_ai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"❌ Error OpenAI: {e}")
        return "Aku lagi error, nanti aku coba lagi ya ❤️"

# Event listener untuk chat masuk
@client.on(events.NewMessage(incoming=True, from_users=TARGET_USER))
async def handler(event):
    msg = event.message.message.lower()

    # Cek kata-kata mood negatif
    mood_negatif = ["sedih", "capek", "kangen", "sendiri", "stress", "galau", "lelah"]
    if any(word in msg for word in mood_negatif):
        mood_prompt = "Kamu adalah cowok yang sangat perhatian dan pengertian. Cewek kamu sedang sedih, jadi balasan harus lembut, menenangkan, dan penuh kasih sayang."
    else:
        mood_prompt = "Kamu adalah pacar yang penyayang dan selalu membalas dengan perhatian."

    reply_text = await chat_ai(f"{mood_prompt}\n\nUser: {msg}\nAI:")
    
    await event.reply(reply_text)

async def main():
    await client.start()
    print("🚀 Bot AI Telegram aktif di Koyeb...")
    asyncio.create_task(send_random_messages())  # Auto-kirim pesan cinta
    await client.run_until_disconnected()

asyncio.run(main())

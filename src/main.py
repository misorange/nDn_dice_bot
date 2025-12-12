import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncpg
import nDnDICE

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
pool = None  # DB接続プール

async def init_db():
    """データベース接続とテーブル作成"""
    global pool
    # DBコンテナが立ち上がるまで少し待つ（簡易的な待機処理）
    await asyncio.sleep(5)
    try:
        pool = await asyncpg.create_pool(
            user=DB_USER, password=DB_PASSWORD, database=DB_NAME, host=DB_HOST
        )
        async with pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS roll_history (
                    id SERIAL PRIMARY KEY,
                    user_name TEXT,
                    command TEXT,
                    result TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        print("Database connected and table ready.")
    except Exception as e:
        print(f"DB Connection Error: {e}")

@bot.event
async def on_ready():
    await init_db()
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # 履歴表示コマンド (!history)
    if message.content == '!history':
        if pool:
            async with pool.acquire() as conn:
                rows = await conn.fetch('SELECT user_name, command, result FROM roll_history ORDER BY id DESC LIMIT 5')
                if rows:
                    msg = "**📜 最近のダイス履歴:**\n"
                    for row in rows:
                        msg += f"・{row['user_name']}: {row['command']} -> {row['result']}\n"
                    await message.channel.send(msg)
                else:
                    await message.channel.send("履歴はまだありません。")
        return

    # ダイス判定
    if nDnDICE.judge_nDn(message.content):
        result_text = nDnDICE.nDn(message.content)
        if result_text:
            await message.channel.send(result_text)
            
            # DBに保存
            if pool:
                async with pool.acquire() as conn:
                    await conn.execute(
                        'INSERT INTO roll_history (user_name, command, result) VALUES ($1, $2, $3)',
                        message.author.display_name, message.content, result_text
                    )

    await bot.process_commands(message)

if __name__ == '__main__':
    bot.run(TOKEN)
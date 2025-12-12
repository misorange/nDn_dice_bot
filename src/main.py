import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import nDnDICE  # nDnDICE.py をインポート

# 環境変数の読み込み
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Botの初期設定 (メッセージ内容を読み取る権限を許可)
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('---------------------------------------------')

@bot.event
async def on_message(message):
    # 自分自身のメッセージには反応しない
    if message.author == bot.user:
        return

    # メッセージ本文を取得
    content = message.content

    # nDnDICEの判定ロジックを使用
    # judge_nDn が True ならサイコロを振る
    if nDnDICE.judge_nDn(content):
        result_text = nDnDICE.nDn(content)
        if result_text:
            await message.channel.send(result_text)

    # 他のコマンド等が動くようにするおまじない
    await bot.process_commands(message)

if __name__ == '__main__':
    if not TOKEN:
        print("Error: DISCORD_TOKEN is not found in environment variables.")
    else:
        bot.run(TOKEN)
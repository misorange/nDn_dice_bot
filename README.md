# Dockerized Discord Dice Bot

Docker Composeで動作する、シンプルなDiscord用ダイスBotのソースコードです。
授業課題の提出用として作成しました。

## 機能
* `ndndice` 構文（例: `2d6`, `1d100`）に反応してダイスを振ります。

## 必要要件
* Docker / Docker Compose
* Discord Bot Token

## 使い方 (Usage)

1. リポジトリをクローンします。
2. `.env.sample` を `.env` にリネームし、あなたのBot Tokenを記述します。
   ```bash
   cp .env.sample .env
   nano .env
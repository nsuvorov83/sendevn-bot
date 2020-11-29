# SENDEVN-BOT
A simple telegram bot for sending records from Telegram with a special e-mail of Evernote.

## Clone
```
git clone https://github.com/nsuvorov83/sendevn-bot.git && cd sendevn-bot
```

## Configure
Edit and remove "_example" in .env_example file . The bot processes messages from CFG_OWNER_ID only. You can learn your telegram user_id using @my_id_bot .
Create a rule in your Outlook as showed in image below to setting tasks automatically.

## Run in docker
```
docker-compose up -d
```

## TODO
- [X] Базовый функционал бота
- [X] Добавление вложений
- [ ] Настройка кредов прямо из бота

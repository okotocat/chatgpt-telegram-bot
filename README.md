# chatgpt-telegram-bot
This is a simple python script that starts telegram bot. Bot is used for connecting to openAI servers and pulling ChatGPT respone generated from user input message.
* OpenAI ChatGPT in your own telegram bot
* Connections to mySQL database, for storing usernames, user_ids, prompt, chatGPT_reply, timestamp.
* Logging usernames, user_ids, prompt, chatGPT_reply, timestamps to a file.

# How to use?
Redefine * signs in api_keys.py for yours tokens and database.

# How it works?
Python script, using [PyTelegramBotApi](https://pypi.org/project/pyTelegramBotAPI/) as api, for connecting to Telegram via api token.
[MySQL-Connector-Python](https://pypi.org/project/mysql-connector-python/) for database connection, and [OpenAI](https://pypi.org/project/openai/) for connection to OpenAI's ChatGPT API.

## Contacts
If you want to help, contribute, request a feature, feel free to PM me in telegram: @tttriot

# Discord Tickets Bot
Add ticket support system to your server (Inspired by [DBS DAO](https://t.me/bomzhuem))

# Install
## Requirements
- Python3.8+
## Dependencies
- discord.py 2.0.0+
## Installation
1. ```sh
    sudo apt update && sudo apt upgrade -y
    sudo apt install git
    git clone git@github.com:Sometimesfunny/discord_tickets_bot.git
    pip3 install -r requirements.txt
    ```
2. Create discord_tickets_config.ini
3. Insert this template:
```ini
[AUTH]
bot_token = 'YOUR_DISCORD_BOT_TOKEN'
```
4. Save file
## Run
```sh
python3 discord_tickets_bot.py
```
# Features
- Add create ticket Button to your server
- Moderate tickets
- Create normal or collaborative tickets
- SHow ticket logs


A discord bot prepared in 72h as a takehome assignment for a hiring process.
The requirements were simple: A bot fetching K-line spot data from Bybit, calculating RSI from the data and announcing the RSI on a discord server

------- IMPORTANT -------
 - For running the bot you will need a Discord Bot token with Send Messages bot permission. Luckily, the exact steps necessary to obtain one were listed on: https://discord.com/developers/docs/quick-start/getting-started
 - To run the bot, you will need to place your bot token and app's client_id in the config.py file. Client_id can be seen in your Discord app's OAUTH2 panel, and the bot token can be generated in your Discord app's BOT panel.
 - You will also need to add the bot to your Discord server.
   Everything is probably explained better in the aforementioned link.

To run the bot, you can either clone the repo and run main.py with shell/IDE or use the Dockerfile to build a Docker image and run docker Containers.
Once the bot is running, in order to get the RSI announcements you need to use command /relative_strength_index, pass in desired timeframe (i.e. 60), period (i.e. 14) and symbol (i.e. SOLUSDT) options.
The bot should then send announcements to the channel where the command had been run. 


------- Notes from author -------

This was fun, a little bit more difficult than i thought. Got to work with different APIs, didn't expect Websocket connections and API to be this different from one another
Things that went wrong and could probably be improved on:

  - WSL2 is terrible and i spend way too much time trying to get Docker to work because of wsl installation errors
  - ... as a result, some things could be improved on:
      - currently there's no way to stop the bot RSI command other than killing the bot - should be added
      - Discord API asks you to send PINGs on your own every once in a while - the bot doesn't do that, but after a while discord asks for a ping anyway and then the bot works fine
      - Discord API recommends checking for a HEARTBEAT ACK response and restarting the connection if you don't get HEARTBEAT ACK after a ping - the bot doesn't do that
      - originally i wanted to split bot, bybit and discord logic into separate files but it all got mixed up. Could've been worse i suppose
      - the bot should be fine with adding more commands, so thats a plus
      - I spent too time much on this
      - K-Line charts are pretty
   

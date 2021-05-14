# Flexbot - Pythonic Discord Bot (ETH Mining Stats)

A Discord.py Bot used to see the stats of your miner account on [Flexpool](https://flexpool.io/) by using their free, public API (v1), along with other Ethereum related statistics, such as the current gas oracle, ETH price et caetera.

## Setup/Prerequisites:

If you intend to use the Discord bot, **TWO** API keys will be required. These can be acquired for free; with limited calls (5/sec) [at this link](https://etherscan.io/apis) for Etherscan on their website, and for using the bot you will need to create a token [at Discord Developers](https://discord.com/developers).
**You should put the API key for Etherscan in the .env file under the key "ETHERSCAN", and the API key for Discord in the .env file under the key "DISCORD".**

In order to run and use this tool, a couple of PyPi libraries are required:

- Discord.py API Wrapper

```python
pip install discord
```

- Requests

```python
pip install requests
```

- REPL.IT Pythonic

```python
pip install replit
```

- Etherscan API Wrapper (Unofficial, Python)

```python
pip install etherscan-python
```

## Usage:

Simply run the "main.py" file once you have placed the API Keys in .env - it should then function like normal.

Thank you for checking out this project.
**Please note that to use the database function in this software, it is required that you run it by creating a repl at replit.com - you may wish to re-jig the database system, however this was most convenient for the small-scope use case I used it for.**

Copyright (c) Aidan Juma 2021 - You may download and use this code for personal use. Any modifications made should be giving credit to the original author (myself) and the editor.

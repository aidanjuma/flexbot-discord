import os
import json
import discord
import requests

from replit import db
from etherscan import Etherscan
from discord.ext import commands

# Discord Client (discord.py)
client = commands.Bot(command_prefix='!')

# Remove Default "!help" Command
client.remove_command("help")

# Get API Key for Etherscan Module
etherscan = Etherscan(os.getenv("ETHERSCAN"))

# API Endpoint for Flexpool
flexpool = "https://flexpool.io/api/v1"


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


##### Custom !help Command: Help & Documentation #####
@client.group(invoke_without_command=True)
async def help(ctx):

    # (Embed) - Help/Documentation:
    help_embed = discord.Embed(
        title="Help/Docs",
        description="These are the commands you can use:",
        color=0x0065FA)

    # !gas field:
    help_embed.add_field(
        name="!gas",
        value="Used to display current slow, normal, and fast-speed gas prices",
        inline=False)

    # !price field:
    help_embed.add_field(
        name="!price",
        value="Used to display the last recorded price of ETH in USD ($) and GBP (£)",
        inline=False)

    # !storeaddress field:
    help_embed.add_field(
        name="!storeaddress <ETH address>",
        value="Used to store your ETH address* - stored in a secured database",
        inline=False)

    # !deleteaddress field:
    help_embed.add_field(
        name="!deleteaddress",
        value="Used to delete stored ETH address from FlexBot's database",
        inline=False)

    # !balance field:
    help_embed.add_field(
        name="!balance** (f)",
        value="Used to display current unpaid balance on Flexpool",
        inline=False)

    # !hashrate field:
    help_embed.add_field(
        name="!hashrate** (f)",
        value="Used to display current unpaid balance on Flexpool",
        inline=False)

    # !revenue field:
    help_embed.add_field(
        name="!revenue** (f)",
        value="Used to display an estimate for revenue today on Flexpool")

    # Footer:
    help_embed.set_footer(
        text="*Flexpool commands (f) will only work if this ETH address is used to mine on Flexpool\n**ETH Address required - see '!storeaddress'"
    )

    await ctx.send(embed=help_embed)


##### End of !help Command #####


##### !gas Command: Gas Prices #####
@client.command()
async def gas(ctx):
    price = etherscan.get_gas_oracle()

    slow = price.get('SafeGasPrice')
    normal = price.get('ProposeGasPrice')
    fast = price.get('FastGasPrice')

    # (Embed) - Gas Prices:
    gas_embed = discord.Embed(
        title="Gas Prices (Gwei)",
        description="The current network gas prices are:",
        color=0x0065FA)
    # Slow Gas Price Field:
    gas_embed.add_field(name="Slow:", value=f"{slow} Gwei")

    # Normal Gas Price Field:
    gas_embed.add_field(name="Normal:", value=f"{normal} Gwei")

    # Fast Gas Price Field:
    gas_embed.add_field(name="Fast", value=f"{fast} Gwei")

    # Footer:
    gas_embed.set_footer(text="Data from Etherscan.io")

    await ctx.send(embed=gas_embed)


##### End of !gas Command #####


##### !price Command: Last Block ETH Price #####
@client.command()
async def price(ctx):
    api = "https://api.exchangeratesapi.io/latest?base=USD"
    rates_response = requests.get(api)
    rates_json = json.loads(rates_response.text)

    price = etherscan.get_eth_last_price()
    usd_string = price["ethusd"]
    usd = float(usd_string)

    rate = rates_json["rates"]["GBP"]
    gbp = usd * rate

    # (Embed) - Last Block ETH Price:
    eth_embed = discord.Embed(
        title="Last Block ETH Price",
        description="The current price of Ethereum (ETH):",
        color=0x0065FA)

    # Price Field (USD):
    eth_embed.add_field(name="United States Dollar ($)", value=f"{usd}")

    # Price Field (GBP):
    eth_embed.add_field(name="Great British Pound (£)",
                        value=f"{round(gbp, 2)}")

    # Footer:
    eth_embed.set_footer(text="Data from Etherscan.io")

    await ctx.send(embed=eth_embed)


##### End of !price Command #####


##### !storeaddress Command: Remember User's ETH Address #####
@client.command()
async def storeaddress(ctx, address, member: discord.Member = None):
    # Used (later) to get the User ID of sender:
    member = ctx.author if not member else member

    # Enters Address with User ID into Replit Database:
    db[f"{member.id}"] = f"{address}"

    await ctx.send(
        f"ETH Address '{address}' has been stored for use with FlexBot commands."
    )


##### End of !storeaddress Command #####


##### !deleteaddress Command: Deletes User's ETH Address from replitdb #####
@client.command()
async def deleteaddress(ctx, member: discord.Member = None):
    # Used (later) to get the User ID of sender:
    member = ctx.author if not member else member

    # Gets ETH Address to be deleted for deletion message:
    address = db[f"{member.id}"]

    # Deletes User's Key in replitdb:
    del db[f"{member.id}"]

    await ctx.send(
        f"ETH Address '{address}' has been removed from FlexBot's database.")


##### End of !deleteaddress Command #####


##### !balance Command: Gets Balance of Stored ETH Address #####
@client.command()
async def balance(ctx, member: discord.Member = None):
    # Used to check database for User ID's ETH Address:
    member = ctx.author if not member else member

    # Gets User's replitdb Stored Address:
    address = db[f"{member.id}"]

    # Checks if User has ETH Address stored:
    if address == "":
        await ctx.send(
            "Uh oh. You don't seem to have an ETH address stored with me. In order to use this command, please store an address using the !storeaddress command - see !help for more details."
        )
    else:
        pass

    # Fetches User's Unpaid Balance from Flexpool API:
    balance_response = requests.get(f"{flexpool}/miner/{address}/balance")
    balance_json = json.loads(balance_response.text)
    balance_text = balance_json["result"]
    balance = int(balance_text) * 10**-18

    await ctx.send((f"Unpaid Balance: {float(round(balance, 6))}ETH"))


##### End of !balance Command #####


##### !hashrate Command: Gets Reported and Effective Hashrates #####
@client.command()
async def hashrate(ctx, member: discord.Member = None):
    # Used to check database for User ID's ETH Address:
    member = ctx.author if not member else member

    # Gets User's replitdb Stored Address:
    address = db[f"{member.id}"]

    # Checks if User has ETH Address stored:
    if address == "":
        await ctx.send(
            "Uh oh. You don't seem to have an ETH address stored with me. In order to use this command, please store an address using the !storeaddress command - see !help for more details."
        )
    else:
        pass

# Fetches User's Hashrate Data from Flexpool API:
    hashrate_response = requests.get(f"{flexpool}/miner/{address}/current")
    hashrate_json = json.loads(hashrate_response.text)

    reported_text = hashrate_json["result"]["reported_hashrate"]
    effective_text = hashrate_json["result"]["effective_hashrate"]

    reported = int(
        reported_text) / 1000000  # Converts hashrates from H/s to MH/s
    effective = int(
        effective_text) / 1000000  # Converts hashrates from H/s to MH/s

    await ctx.send(
        f"Reported Hashrate: {float(round(reported, 2))}MH/s, Effective Hashrate: {float(round(effective, 2))}MH/s"
    )


##### End of !hashrate Command #####


##### !revenue Command: Gets Estimated Daily Revenue on Flexpool #####
@client.command()
async def revenue(ctx, member: discord.Member = None):
    # Used to check database for User ID's ETH Address:
    member = ctx.author if not member else member

    # Gets User's replitdb Stored Address:
    address = db[f"{member.id}"]

    # Checks if User has ETH Address stored:
    if address == "":
        await ctx.send(
            "Uh oh. You don't seem to have an ETH address stored with me. In order to use this command, please store an address using the !storeaddress command - see !help for more details."
        )
    else:
        pass

    # Gets Daily Revenue Data from Flexpool API:
    revenue_response = requests.get(
        f"{flexpool}/miner/{address}/estimatedDailyRevenue")
    revenue_json = json.loads(revenue_response.text)

    revenue_text = revenue_json["result"]
    revenue = int(revenue_text) * 10**-18

    await ctx.send(f"Today's Estimated Earnings: {float(round(revenue, 6))}ETH"
                   )


##### End of !revenue Command #####

# Bot Token Reference ("DISCORD")
client.run(os.getenv("DISCORD"))

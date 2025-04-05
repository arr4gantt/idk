import discord
from discord.ext import commands

# Prediction function
def predict(ping: int):
    regular = 0.001 * ping + 0.037
    linear = 0.0011 * ping + 0.025
    slope = 0.002 * ping

    if ping < 85:
        stepwise = 0.118 + ((ping - 80) * 0.0011)
    elif ping < 90:
        stepwise = 0.1224 + ((ping - 84) * 0.0011)
    else:
        stepwise = 0.129 + ((ping - 90) * 0.0016)

    fraction = (ping + 3.5) / 660

    a = -2.37037e-06
    b = 0.000934074
    c = 0.07092963
    complex_pred = a * ping ** 2 + b * ping + c

    slope_pred = 0.002 * ping

    # Format response message
    response = f"**Average Ping {ping}ms**:\n"
    response += f"    Regular_Prediction = {regular:.10f}\n"
    response += f"    Linear_Prediction = {linear:.10f}\n"
    response += f"    Stepwise_Prediction = {stepwise:.10f}\n"
    response += f"    Fraction_Prediction = {fraction:.10f}\n"
    response += f"    Complex_Prediction = {complex_pred:.10f}\n"
    response += f"    Slope_Prediction = {slope_pred:.15f}"
    
    return response

# Set up bot command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# When the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# When a message is received
@bot.event
async def on_message(message):
    # Don't let the bot reply to itself
    if message.author == bot.user:
        return

    if message.content.startswith("!pred"):
        try:
            # Extract ping value from the command
            ping_value = int(message.content.split()[1])
            response = predict(ping_value)

            # Send prediction in a DM
            await message.author.send(response)

        except (IndexError, ValueError):
            await message.author.send("Please use the format: `!pred [ping_value]`")

    await bot.process_commands(message)

# Run the bot with your token
bot.run('tokn')

import discord
import responses
from user import User


# Dictionary to store user objects
users = {}

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True


# Send messages
async def send_message(message, user_message, is_private):
    try:
        user_id = str(message.author.id)
        user = users.get(user_id)

        if not user:
            user = User(user_id)
            users[user_id] = user

        user.add_message(user_message, is_private)
        response = responses.generate_response(user)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = 'MTEzNjIxOTg0Mzc1MDc5MzI1Ng.G1QAnE.Fgds0NXx8dOwquF5EYQm6uclwBBkxW4qQUsrQE'
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        # Make sure the bot doesn't get stuck in an infinite loop
        if message.author == client.user:
            return

        # Get data about the user
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        is_private = isinstance(channel, discord.DMChannel)

        # Debug printing
        print(f"{username} said: '{user_message}' ({channel})")

        await send_message(message, user_message, is_private)

    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)
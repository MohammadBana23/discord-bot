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
    TOKEN = 'MTEzNjIxOTg0Mzc1MDc5MzI1Ng.GOWUY5.vFNiFpQe11IN2mKhaSomXqsfT8CRMBv5bXUga8'
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        # Ignore messages sent by the bot itself
        if message.author == client.user:
            return
        
        # Get data about the user
        user_message = str(message.content)
        channel = str(message.channel)
        is_private = isinstance(channel, discord.DMChannel)

        if message.content.startswith('!ban'):
            # Check if the author of the message has the "Ban Members" permission
            if message.author.guild_permissions.ban_members:
                # Split the message content to get the user to ban
                user_to_ban = message.content.split(' ')[1]
                try:
                    # Get the member object for the user to ban
                    member = await message.guild.fetch_member(int(user_to_ban))
                    # Ban the user
                    await member.ban()
                    await message.channel.send(f'{member.display_name} has been banned.')
                except discord.errors.NotFound:
                    await message.channel.send('User not found.')
            else:
                await message.channel.send('You don\'t have permission to ban members.')
        elif message.content.startswith('!unban'):
            # Assuming the bot has the "Ban Members" permission
            user_id = message.content.split(' ')[1]
            banned_users = message.guild.bans()
            async for ban_entry in banned_users:
                if ban_entry.user.id == int(user_id):
                    await message.guild.unban(ban_entry.user)
                    await message.channel.send(f'{ban_entry.user.name} has been unbanned.')
                    return

            await message.channel.send('User not found or not banned.')
        elif message.content.startswith('!mute'):
            # Assuming the bot has the "Manage Roles" permission
            user_id = message.content.split(' ')[1]
            user = message.guild.get_member(int(user_id))
            
            if user:
                # Find the "Muted" role or create it if it doesn't exist
                muted_role = discord.utils.get(message.guild.roles, name="Muted")
                if not muted_role:
                    print("Muted role not found, creating...")
                    try:
                        muted_role = await message.guild.create_role(name="Muted", reason="Muted user role")
                        print("Muted role created successfully.")
                    except discord.errors.Forbidden:
                        print("The bot does not have the 'Manage Roles' permission to create the role.")
                else:
                    print("Muted role found.")
                
                # Add the "Muted" role to the user
                await user.add_roles(muted_role)

                # Set the permissions for the "Muted" role to prevent sending messages
                for channel in message.guild.text_channels:
                    await channel.set_permissions(muted_role, send_messages=False)
                
                await message.channel.send(f'{user.display_name} has been muted and cannot send messages.')
            else:
                await message.channel.send('User not found.')

        else:
            await send_message(message, user_message, is_private)
    # @client.event
    # async def on_message(message):
    #     # Make sure the bot doesn't get stuck in an infinite loop
    #     if message.author == client.user:
    #         return

    #     # Get data about the user
    #     username = str(message.author)
    #     user_id = str(message.author.id)
    #     user_message = str(message.content)
    #     channel = str(message.channel)
    #     is_private = isinstance(channel, discord.DMChannel)

    #     # Debug printing
    #     print(f"{username} said: '{user_message}' ({channel})")

    #     # Check if the user is trying to grant or revoke access
    #     if user_message.startswith('!grant_access'):
    #         # For simplicity, we are setting access level 1 if the command is '!grant_access'
    #         user = users.get(user_id)
    #         if user:
    #             user.access_level = 1
    #             await message.channel.send('Access granted!')
    #         else:
    #             await message.channel.send('You need to start a conversation with the bot first.')

    #     elif user_message.startswith('!revoke_access'):
    #         # For simplicity, we are revoking all access if the command is '!revoke_access'
    #         user = users.get(user_id)
    #         if user:
    #             user.access_level = 0
    #             await message.channel.send('Access revoked!')
    #         else:
    #             await message.channel.send('You need to start a conversation with the bot first.')

    #     else:
    #         await send_message(message, user_message, is_private)

    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)
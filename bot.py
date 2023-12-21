"""
 __  __       _ _   _
|  \/  |_   _| | |_(_)      ___  ___ _ ____   _____ _ __
| |\/| | | | | | __| |_____/ __|/ _ \ '__\ \ / / _ \ '__|
| |  | | |_| | | |_| |_____\__ \  __/ |   \ V /  __/ |
|_|  |_|\__,_|_|\__|_|     |___/\___|_|    \_/ \___|_|
 ____  _                       _    ____ _           _
|  _ \(_)___  ___ ___  _ __ __| |  / ___| |__   __ _| |_
| | | | / __|/ __/ _ \| '__/ _` | | |   | '_ \ / _` | __|
| |_| | \__ \ (_| (_) | | | (_| | | |___| | | | (_| | |_
|____/|_|___/\___\___/|_|  \__,_|  \____|_| |_|\__,_|\__|

    ________________________________
    < by Brais__, Apache 2.0 License >
    --------------------------------
        \
        \
            oO)-.                       .-(Oo
            /__  _\                     /_  __\
            \  \(  |     ()~()         |  )/  /
            \__|\ |    (-___-)        | /|__/
            '  '--'    ==`-'==        '--'  '
"""
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from utils import db, logger
import asyncio
import logging
import os
from profanityfilter import ProfanityFilter

pf = ProfanityFilter()

def censor_profanity(text):
    return pf.censor(text)

intents = nextcord.Intents.default()
intents.message_content = True  # This intent is necessary to access the content of messages, it must also be enabled in https://discord.com/developers/applications/APP-ID/bot

bot = commands.Bot(command_prefix="!", intents=intents)

logger.setup_logging()
log = logging.getLogger(__name__)   

@bot.event
async def on_ready():
    log.info(f'Logged in as {bot.user.name}')


#        COMMANDS
    
@bot.slash_command(name="setrelaychannel", description="Set a channel as the relay channel for this server.")
@commands.has_permissions(administrator=True)
async def set_relay_channel(interaction: Interaction, 
                            channel: nextcord.TextChannel = SlashOption(description="Select a channel"),
                            slowmode_delay: int = SlashOption(description="Set the slow mode delay in seconds", required=False, default=5)):
    """
    Set a channel as the relay channel for the server. This channel will handle relayed messages.

    Parameters:
    interaction (Interaction): The context of the Discord interaction.
    channel (nextcord.TextChannel): The channel to be set as the relay channel.
    slowmode_delay (int): The slow mode delay in seconds for the channel.

    Notes:
    Requires administrator permissions. The bot must have 'Manage Channels' permission to set slow mode.
    """
    log.info(f"User {interaction.user.name} with ID {interaction.user.id} executed /setrelaychannel {channel}")
    try:
        # Check if the bot has the required permissions to manage the channel
        if not channel.permissions_for(interaction.guild.me).manage_channels:
            log.warning("Bot does not have permission to manage the channel.")
            await interaction.response.send_message(
                "⚠️ I don't have permission to set slow mode for channels. "
                "Please ensure I have the 'Manage Channels' permission. "
                "This permission is required to use the relay channel functionality.", # They can disable slow mode after without any consequences but I'll work on that later
                ephemeral=True
            )
            return

        # Set the slow mode delay for the channel (5s by default)
        await channel.edit(slowmode_delay=slowmode_delay)
        await db.update_server_setting(str(interaction.guild.id), "relay_channel_id", str(channel.id))
        await db.update_server_setting(str(interaction.guild.id), "display_name", interaction.guild.name)
        await interaction.response.send_message(
            f"Relay channel set to {channel.mention} with a slow mode delay of {slowmode_delay} seconds"
        )
    except nextcord.Forbidden:
        log.warning("Bot does not have permission to edit channel settings.")
        await interaction.response.send_message(
            "⚠️ I don't have permission to edit this channel's settings. "
            "Please give me the 'Manage Channels' permission and try again.",
            ephemeral=True
        )
    except nextcord.HTTPException as e:
        log.exception("Failed to set slow mode on the channel")
        await interaction.response.send_message(
            "Failed to set slow mode due to an HTTP error.",
            ephemeral=True
        )



@bot.slash_command(name="setdisplayname", description="Set the display name for this server in the relay.")
@commands.has_permissions(administrator=True)
async def set_display_name(interaction: Interaction, display_name: str = SlashOption(description="Enter the new display name")):
    """
    Set the display name for the server.

    Parameters:
    interaction (Interaction): The context of the Discord interaction.
    display_name (str): The new display name for the server.

    Notes:
    Requires administrator permissions.
    """
    log.info(f"User {interaction.user.name} with ID {interaction.user.id} executed /setdisplayname {display_name}")
    await db.update_server_setting(str(interaction.guild.id), "display_name", display_name)
    await interaction.response.send_message(f"Display name set to {display_name}")



@bot.slash_command(name="listconnectedservers", description="Lists all servers connected by the relay.")
async def list_connected_servers(interaction: Interaction):
    """
    Lists all servers connected by the relay.

    Parameters:
    interaction (Interaction): The context of the Discord interaction.

    Notes:
    Does not require administrator permissions, users will be able to see and join other servers if they added an invite link.
    """
    log.info(f"User {interaction.user.name} with ID {interaction.user.id} executed /listconnectedservers")
    try:
        server_settings = await db.get_all_server_settings()
        if not server_settings:
            await interaction.response.send_message("No servers are currently connected.", ephemeral=True)
            return

        message = "## Connected Servers:\n"
        for server_id, settings in server_settings.items():
            server = bot.get_guild(int(server_id))

            if settings.get("display_name"):
                message += f"### {settings['display_name']}\n"
            elif server:
                message += f"### {server.name}\n"
            else:
                # If the server object could not be retrieved, log an error and display a placeholder
                log.error(f"Could not retrieve the server object for server ID {server_id}.")
                message += f"Name not found. Check bot logs for details.\n"

            if settings.get("description"):
                message += f"  **Description:** {settings['description']}\n"
            if settings.get("invite_link"):
                message += f"  **Invite Link:** {settings['invite_link']}\n"

        await interaction.response.send_message(message, ephemeral=True)
    except Exception as e:
        log.exception("An error occurred while listing connected servers")
        await interaction.response.send_message("An error occurred while retrieving the server list.", ephemeral=True)



@bot.slash_command(guild_ids=[652892795488698368], name="setserverdescription", description="Set the description for this server.")
@commands.has_permissions(administrator=True)
async def set_server_description(interaction: Interaction, description: str = SlashOption(description="Enter the server description")):
    """
    Set the description for the server.

    Parameters:
    interaction (Interaction): The context of the Discord interaction.
    description (str): The description of the server.

    Notes:
    Requires administrator permissions. The description is used in the relay system but it is optional.
    """
    log.info(f"User {interaction.user.name} with ID {interaction.user.id} executed /setserverdescription {description}")
    await db.update_server_setting(str(interaction.guild.id), "description", description)
    await interaction.response.send_message(f"Description set for the server.")



@bot.slash_command(guild_ids=[652892795488698368], name="setserverinvite", description="Set the invite link for this server.")
@commands.has_permissions(administrator=True)
async def set_server_invite(interaction: Interaction, invite_link: str = SlashOption(description="Enter the server invite link")):
    """
    Set the invite link for the server.

    Parameters:
    interaction (Interaction): The context of the Discord interaction.
    invite_link (str): The invite link of the server.

    Notes:
    Requires administrator permissions. The invite link is used in the relay system for server who want to allow other users to join. Also optional.
    """
    log.info(f"User {interaction.user.name} with ID {interaction.user.id} executed /setserverinvite {invite_link}")
    await db.update_server_setting(str(interaction.guild.id), "invite_link", invite_link)
    await interaction.response.send_message(f"Invite link set for the server.")



@bot.slash_command(name="toggleprofanityfilter", description="Toggles the profanity filter for this server.")
@commands.has_permissions(administrator=True)
async def toggle_profanity_filter(interaction: Interaction):
    """
    Toggles the profanity filter for the server.
    Requires administrator permissions.
    """
    # Retrieve all server settings
    all_settings = await db.get_all_server_settings()
    server_settings = all_settings.get(str(interaction.guild.id), {})
    current_setting = server_settings.get("profanity_filter_enabled", 0)
    
    # Toggle the setting
    new_setting = 0 if current_setting else 1
    
    # Update the setting in the database
    await db.update_server_setting(str(interaction.guild.id), "profanity_filter_enabled", new_setting)
    
    # Send a confirmation message
    status = "enabled" if new_setting else "disabled"
    await interaction.response.send_message(f"Profanity filter has been {status}.")


@bot.event
async def on_message(message):
    try:
        if message.author.bot or message.webhook_id:
            return  # Ignore bot and webhook messages

        server_settings = await db.get_server_settings(str(message.guild.id))
        if server_settings and server_settings.get("relay_channel_id") == str(message.channel.id):
            display_name = server_settings.get("display_name", message.guild.name)
            log.info(f"Creating task for message {message.id} in {display_name}/{message.guild.name}")
            asyncio.create_task(relay_messages(message, display_name))

        await bot.process_commands(message)
    except Exception as e:
        log.error(f"Error in on_message: {e}", exc_info=True)

async def relay_messages(message, display_name):
    try:
        all_server_settings = await db.get_all_server_settings()
        for server_id, settings in all_server_settings.items():
            if server_id != str(message.guild.id):  # Avoid sending back to the originating server
                target_channel_id = settings.get("relay_channel_id")
                if target_channel_id:
                    target_channel = bot.get_channel(int(target_channel_id))
                    if target_channel:
                        log.info(f"Starting webhook task task for message {message} from {display_name} to server {server_id}")
                        asyncio.create_task(relay_message_to_webhook(message, display_name, target_channel))
    except Exception as e:
        log.error(f"Error in relay_messages: {e}", exc_info=True)


async def relay_message_to_webhook(message, server_display_name, target_channel):
    try:
        # Retrieve the profanity filter setting for the server
        server_settings = await db.get_server_settings(str(message.guild.id))
        profanity_filter_enabled = server_settings.get("profanity_filter_enabled", 0)

        # Censor the content if the profanity filter is enabled
        if profanity_filter_enabled:
            censored_content = censor_profanity(message.content)
        else:
            censored_content = message.content

        # Check if the message is empty after censoring (skip if it is)
        if not censored_content.strip() and not message.attachments:
            return

        webhooks = await target_channel.webhooks()
        webhook = next((wh for wh in webhooks if wh.user == bot.user), None)
        if not webhook:
            webhook = await target_channel.create_webhook(name="Multi-Server Relay")

        webhook_name = f"{message.author.display_name} [{server_display_name}]"
        webhook_avatar = message.author.display_avatar.url if message.author.avatar else None
        files = [await attachment.to_file() for attachment in message.attachments] if message.attachments else None

        await webhook.send(
            content=censored_content,
            username=webhook_name,
            avatar_url=webhook_avatar,
            files=files
        )

        # Log message to the database
        # REMOVED DUE TO PRIVACY CONCERNS,
        # please give feedback if you think it would be ok to have it
        """
        await db.log_message(
            server_id=str(message.guild.id),
            server_display_name=server_display_name,
            username=message.author.display_name,
            message_id=str(message.id),
            content=message.clean_content,
            timestamp=message.created_at.isoformat()  # Use Discord's timestamp
        )
        """
    except nextcord.HTTPException as e:
        if e.status == 429:
            log.warning("We are being rate limited!")
        else:
            log.exception("HTTPException occurred while sending a webhook message")
    except Exception as e:
        log.exception("An unexpected error occurred while sending a webhook message")

if __name__ == "__main__":
    asyncio.run(db.initialize_db())
    bot_token = os.getenv('DISCORD_TOKEN')
    bot.run(bot_token)

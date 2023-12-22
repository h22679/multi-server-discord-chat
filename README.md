# Multi-server Discord Chat
The Multi-Server Discord Chat bot allows users to communicate in a text channel that connects multiple servers. It's built using [nextcord](https://docs.nextcord.dev/en/stable/), [aiosqlite](https://pypi.org/project/aiosqlite/) and [profanityfilter](https://github.com/areebbeigh/profanityfilter).

### You have two options for using this bot:

1. **Deploy Your Own Bot**: You can deploy your instance of the bot to facilitate communication within your specific set of servers.

2. **Invite a Running Instance**: Alternatively, you can invite an already running instance of this bot to connect to your servers.

### Make sure to grant the bot the following permissions for proper functionality:

- Manage Channels
- Manage Webhooks
- Enable the message content intent.

## Getting Started

When you first invite the bot to a server, ensure you use the `/setrelaychannel` command to start communicating with other servers. Here are some other available commands:

- `/setdisplayname`: Customize the server name for relay channels instead of using the guild name.
- `/setserverdescription`: Add a description for your server.
- `/setserverinvite`: Include an invite link for your server.
- `/listconnectedservers`: Get a list of currently connected servers.
- `/toggleprofanityfilter`: Enable or disable the profanity filter, applicable only to incoming messages.

Message logs are disabled (I simply commented the part I used to keep logs during testing) since I'm not sure if it would be ok to keep logs, to which extent it would be ok (how much information to collect) or if it would be helpful or effective at all for moderation actions, feel free to give me your feedback on this.
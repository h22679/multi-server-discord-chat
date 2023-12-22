# multi-server-discord-chat
Bot thats allows users to communicate in a text channel that connects multiple servers.

You can deploy your own bot to communicate with your own set of servers or invite an already running instance of this bot to connect to those servers.

The bot needs `Manage Channels` and `Manage Webhooks` permissions and the message content intent to be enabled to work properly.

When you first invite it to a server you must use `/setrelaychannel` for it to start working. Other available commands are:

- `/setdisplayname` Allows you to set a custom server name for the relay channels instead of using the guild name.
- `/setserverdescription` Allows you to add a description for your server.
- `/setserverinvite` Allows you to add an invite link to your server.
- `/listconnectedservers` Sends a list of currently connected servers.
- `/toggleprofanityfilter` Enable/disble profanity filter. Only works on incoming messages.


Message logs are disabled (I simply commented the part I used to keep logs during testing) since I'm not sure if it would be ok to keep logs, to which extent it would be ok (how much information to collect) or if it would be helpful or effective at all for moderation actions, feel free to give me your feedback on this.
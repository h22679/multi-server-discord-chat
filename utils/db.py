# To be honest, this whole thing could have probably be done better but i dont like working with databases.
# Message logging does not work since im not sure if it would be ok to keep message logs or how effective
# they would be to take moderation actions, feel free to give your feedback.
import aiosqlite
from utils import logger
import logging
import os

logger.setup_logging()
log = logging.getLogger(__name__)   

# Define the path to the data directory relative to the location of db.py
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# Create the data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

# Define the path for the database file
DATABASE_PATH = os.path.join(DATA_DIR, 'multiserver_chat.db')

async def initialize_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS server_settings (
                server_id TEXT PRIMARY KEY,
                relay_channel_id TEXT,
                display_name TEXT,
                description TEXT,
                invite_link TEXT,
                profanity_filter_enabled INTEGER DEFAULT 0
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS message_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                server_id TEXT,
                server_display_name TEXT,
                username TEXT,
                message_id TEXT,
                content TEXT,
                timestamp DATETIME
            )
        ''')
        await db.commit()

async def update_server_setting(server_id, setting_name, setting_value):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(f'''
            INSERT INTO server_settings (server_id, {setting_name}) VALUES (?, ?)
            ON CONFLICT(server_id) DO UPDATE SET {setting_name} = excluded.{setting_name}
        ''', (server_id, setting_value))
        await db.commit()

async def log_message(server_id, server_display_name, username, message_id, content, timestamp):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            INSERT INTO message_logs (server_id, server_display_name, username, message_id, content, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (server_id, server_display_name, username, message_id, content, timestamp))
        await db.commit()

async def get_server_settings(server_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT relay_channel_id, display_name, profanity_filter_enabled FROM server_settings WHERE server_id = ?', (server_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                settings = {"relay_channel_id": row[0], "display_name": row[1], "profanity_filter_enabled": row[2]}
                log.info(f"Settings retrieved: {settings}")
                return {"relay_channel_id": row[0], "display_name": row[1], "profanity_filter_enabled": row[2]}
            return {}

async def get_all_server_settings():
    settings = {}
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute('SELECT server_id, relay_channel_id, display_name, description, invite_link, profanity_filter_enabled FROM server_settings') as cursor:
            async for row in cursor:
                settings[row[0]] = {
                    "relay_channel_id": row[1],
                    "display_name": row[2],
                    "description": row[3],
                    "invite_link": row[4],
                    "profanity_filter_enabled": row[5]
                }
    log.info(f"Settings retrieved: {settings}")
    return settings

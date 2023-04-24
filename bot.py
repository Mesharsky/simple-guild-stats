import os

import discord
from discord.ext import commands
from discord.embeds import Embed
from dotenv import load_dotenv

from db_manager import DBManager
from adminroles import AdminRolesList

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True


class GuildStatsBot(commands.Bot):
    def __init__(self):
        self.db = DBManager('guild_stats.db')
        self.admin_roles = AdminRolesList()

        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self):
        await self.tree.sync()
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def setup_hook(self):
        for filename in os.listdir("./commands"):
            if filename.endswith(".py"):
                try:
                    await self.load_extension(f"commands.{filename[:-3]}")
                    print(f"Loaded command {filename}")
                except Exception as e:
                    print(f"Failed to load command {filename}")
                    print(f"[ERROR] {e}")

        await self.tree.sync()
        print("Successfully synced commands")
        print(f"Logged onto {self.user}")

    async def on_guild_available(self, server: discord.guild):
        results = self.db.query(f'''SELECT role_id FROM adminroles WHERE guild_id = {server.id} ''')

        if results is None or len(results) == 0:
            return

        self.admin_roles.load_server_roles(server, results)

        print(f'Found roles for guild: {server.id} - {server.name}')

    async def on_guild_unavailable(self, server: discord.guild):
        self.admin_roles.clear_server_roles(server) 


bot = GuildStatsBot()

load_dotenv()
bot.run(os.getenv('DISCORD_TOKEN'))

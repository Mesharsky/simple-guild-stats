import discord
from discord import app_commands
from discord.ext import commands


class CheckPointsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='check_points', description='Check points for specific member')
    async def command_check_points(self, interaction: discord.Interaction, member: discord.Member):
        
        guild_id = interaction.guild_id
        if guild_id is None:
            await interaction.response.send_message("There was a problem sending the command. (Unknown guild id).")
            return

        self.bot.db.connect()
        self.bot.db.execute(f'''SELECT points FROM users WHERE guild_id = {guild_id} AND member_id = {member.id}''')

        results = self.bot.db.cursor.fetchone()
        self.bot.db.close()

        member_name = member.nick if member.nick is not None else member.name

        if member is None:
            await interaction.response.send_message(f"Could not find the member {member.name}")
            return
        
        if results is None or results[0] == 0:
            await interaction.response.send_message(f"**{member_name}** has no points")
            return
        
        await interaction.response.send_message(f"**{member_name}** has **{results[0]}** Points")


async def setup(bot):
    await bot.add_cog(CheckPointsCog(bot))

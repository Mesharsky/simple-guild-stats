import discord
from discord import app_commands
from discord.ext import commands


class RemovePointsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='remove_points', description='Remove points for specific member')
    async def command_remove_points(self, interaction: discord.Interaction, member: discord.Member, value: int):

        if not await self.bot.admin_roles.user_has_admin_role(interaction):
            return
        
        guild_id = interaction.guild_id
        if guild_id is None:
            await interaction.response.send_message("There was a problem sending the command. (Unknown guild id).")
            return

        self.bot.db.connect()
        self.bot.db.execute(f'''SELECT points FROM users WHERE guild_id = {guild_id} AND member_id = {member.id}''')
        results = self.bot.db.cursor.fetchone()

        member_name = member.nick if member.nick is not None else member.name

        if results is None or results[0] == 0:
            self.bot.db.close()
            await interaction.response.send_message(f"{member_name} has no points to remove")
            return

        new_points = results[0] - value if value <= results[0] else 0

        self.bot.db.execute(f'''
            UPDATE users SET points = {new_points} WHERE guild_id = {guild_id} AND member_id = {member.id}
            ''')

        rowcount = self.bot.db.rowcount()
        self.bot.db.close()

        if rowcount == 0:
            await interaction.response.send_message(f"Couldnt remove points for {member_name}")
        else:
            await interaction.response.send_message(f"Removed **{value}** points from <@{member.id}>, they have **{new_points}** points left.")


async def setup(bot):
    await bot.add_cog(RemovePointsCog(bot))

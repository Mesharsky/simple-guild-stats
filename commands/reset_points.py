import discord
from discord import app_commands
from discord.ext import commands


class ResetPointsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='reset_points', description='Reset Points For Member')
    async def command_reset_points(self, interaction: discord.Interaction, user: discord.User):
        
        if not await self.bot.admin_roles.user_has_admin_role(interaction):
            return

        guild_id = interaction.guild_id
        if guild_id is None:
            await interaction.response.send_message("There was a problem sending the command. (Unknown guild id).")
            return
        
        self.bot.db.connect()
        self.bot.db.execute(f'''UPDATE users SET points = 0 WHERE guild_id = {guild_id} AND member_id = {user.id}''')
        rowcount = self.bot.db.rowcount()

        self.bot.db.close()

        member_name = user.name

        if rowcount == 0:
            await interaction.response.send_message(f"**{member_name}** has no points to reset")
            return
        
        await interaction.response.send_message(f"Points were reset for {member_name}#{user.discriminator}")


async def setup(bot):
    await bot.add_cog(ResetPointsCog(bot))

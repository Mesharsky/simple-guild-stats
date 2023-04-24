import discord
from discord import app_commands
from discord.ext import commands


class AddPointsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='add_points', description='Add points for specific member')
    async def command_add_points(self, interaction: discord.Interaction, member: discord.Member, value: int):

        if not await self.bot.admin_roles.user_has_admin_role(interaction):
            return
        
        guild_id = interaction.guild_id
        if guild_id is None:
            await interaction.response.send_message("There was a problem sending the command. (Unknown guild id).")
            return

        self.bot.db.query(f'''
            INSERT INTO users (
                guild_id,
                member_id,
                member_name,
                points
            ) VALUES (
                {guild_id},
                {member.id},
                '{member.name}',
                {value}
            ) ON CONFLICT(guild_id, member_id) DO UPDATE SET points = points + {value}''')

        await interaction.response.send_message(f"You succesfully added **{value}** Points for <@{member.id}>")


async def setup(bot):
    await bot.add_cog(AddPointsCog(bot))
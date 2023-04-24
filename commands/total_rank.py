import discord
from discord import app_commands
from discord.ext import commands


class TotalRankCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='total_rank', description='List members ranked by total points')
    async def command_total_rank(self, interaction: discord.Interaction):
        if not await self.bot.admin_roles.user_has_admin_role(interaction):
            return
        
        guild_id = interaction.guild_id
        if guild_id is None:
            await interaction.response.send_message("There was a problem sending the command. (Unknown guild id).")
            return

        # Query the total points earned by each member and order them by descending points
        result = self.bot.db.query(f'SELECT member_name, points FROM users WHERE guild_id = {guild_id} ORDER BY points DESC')

        # Create the embed
        embed = discord.Embed(title='Top Points Members:', color=0x00FF00)

        # Add the top 3 members to the embed as bold text with icons
        top_3 = ''
        for i, (member_name, points) in enumerate(result[:3], start=1):
            icon = '🥇' if i == 1 else '🥈' if i == 2 else '🥉'
            top_3 += f'**{icon} {member_name}: {points}**\n'
        embed.add_field(name='Top 3', value=top_3, inline=False)

        # Add the remaining members to the embed without icons or bold text
        other_members = ''
        for i, (member_name, points) in enumerate(result[3:], start=4):
            member_str = f'{i}. {member_name}: {points}\n'
            if len(other_members + member_str) > 1024:
                break
            other_members += member_str
        embed.add_field(name='Other Members', value=other_members, inline=False)

        # Add the total points earned by all members to the footer
        total_points = self.bot.db.query(f'SELECT SUM(points) FROM users WHERE guild_id = {guild_id}')[0][0]
        embed.set_footer(text=f'Total points earned: {total_points}')

        # Send the embed as a message
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(TotalRankCog(bot))


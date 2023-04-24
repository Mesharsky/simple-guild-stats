import datetime

import discord
from discord import app_commands
from discord.ext import commands


class AwardVoiceMembersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='award_voice_members', description='Award Members Put Title and Reward you want to give out to all members')
    async def command_award_voice_members(self, interaction: discord.Interaction, title: str, points_reward: int):

        if not await self.bot.admin_roles.user_has_admin_role(interaction):
            return
        
        guild_id = interaction.guild_id
        if guild_id is None:
            await interaction.response.send_message("There was a problem sending the command. (Unknown guild id).")
            return
        
        voice_state = interaction.user.voice
        if voice_state is None or voice_state.channel is None:
            await interaction.response.send_message("You need to be in a voice channel to use this command.")
            return
        
        voice_channel = voice_state.channel

        members = voice_channel.members
        members_with_points = []
        points_added = 0

        for member in members:
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
                    {points_reward}
                ) ON CONFLICT(member_id) DO UPDATE SET points = points + {points_reward}''')

            points_added += points_reward
            members_with_points.append(member)

        mentions = [f"{member.mention}" for member in members_with_points]
        
        embed = discord.Embed(title=f"{title} Report", color=0x00FF00)
        embed.add_field(name="Attendance made by\n", value=interaction.user.mention, inline=False)
        embed.add_field(name="Players that got rewarded:", value="\n".join(mentions), inline=False)
        embed.add_field(name="Members Awarded:", value=len(members), inline=False)
        embed.add_field(name="Total Points Added:", value=points_added, inline=False)

        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        embed.set_footer(text=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}   Time: {current_time}")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(AwardVoiceMembersCog(bot))

import random
import discord
from discord import app_commands
from discord.ext import commands

secret_numbers = {}


class ResetAllPointsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='reset_all_points', description='Reset Points For Every Member')
    async def command_reset_all_points(self, interaction: discord.Interaction, security_number: int=None):
        global secret_numbers

        if not await self.bot.admin_roles.user_has_admin_role(interaction):
            return
        
        guild_id = interaction.guild_id
        if guild_id is None:
            await interaction.response.send_message("There was a problem sending the command. (Unknown guild id).")
            return

        if guild_id not in secret_numbers.keys():
            regenerate_secret(secret_numbers, guild_id)

        if security_number is None:
            await interaction.response.send_message(f"To remove points for all members, use the command again with the secret number **{secret_numbers[guild_id]}**")
            return

        elif security_number != secret_numbers[guild_id]:
            await interaction.response.send_message(f"Incorrect security number.\nTo remove points for all members, use the command again with the secret number **{secret_numbers[guild_id]}**")
            return

        regenerate_secret(secret_numbers, guild_id)

        self.bot.db.query(f"UPDATE users SET points = 0 WHERE guild_id = {guild_id}")

        await interaction.response.send_message("Points for all members have been reset!")


def regenerate_secret(secrets: dict, guild_id: int):
    secrets[guild_id] = random.randint(100_000, 1_000_000)


async def setup(bot):
    await bot.add_cog(ResetAllPointsCog(bot))


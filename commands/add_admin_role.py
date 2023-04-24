import discord
from discord import app_commands
from discord.ext import commands


class AddAdminRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='add_admin_role', description='Add role that can use bot commands')
    async def command_add_admin_role(self, interaction: discord.Interaction, role: discord.Role):
        author = interaction.user

        has_admin = False
        for r in author.roles:
            if r.permissions.administrator:
                has_admin = True
                break
        
        if not has_admin:
            await interaction.response.send_message("You need administrator permissions to add a role to the bot.")
            return

        guild_id = interaction.guild_id
        if guild_id is None:
            await interaction.response.send_message("There was a problem sending the command. (Unknown guild id).")
            return

        self.bot.db.query(f'''
            INSERT INTO adminroles (
                guild_id,
                role_id
            ) VALUES (
                {guild_id},
                {role.id}
            )''')

        self.bot.admin_roles.add_role(guild_id, role.id)

        await interaction.response.send_message(f"Role Added: <@&{role.id}>")


async def setup(bot):
    await bot.add_cog(AddAdminRoleCog(bot))
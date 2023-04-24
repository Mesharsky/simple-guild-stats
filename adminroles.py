import discord

class AdminRolesList:
    def __init__(self):
        # Maps dicord.Guild.id to list of discord.Role.id
        self.admin_roles = {}

    async def user_has_admin_role(self, interaction: discord.Interaction):
        author = interaction.user
        guild_id = interaction.guild_id

        if guild_id not in self.admin_roles.keys():
            await interaction.response.send_message("You need to add an admin role before using this command (/add_admin_role)")
            return False

        author_admin_roles = [ role for role in author.roles if role.id in self.admin_roles[guild_id] ]

        if len(author_admin_roles) == 0:
            await interaction.response.send_message("You don't have permission to use that command.")
            return False

        return True

    def add_role(self, guild_id: int, role_id: int):
        if guild_id not in self.admin_roles.keys():
            self.admin_roles[guild_id] = []

        self.admin_roles[guild_id].append(role_id)

    def load_server_roles(self, server: discord.guild, roles: list[tuple[int]]):
        for role in roles:
            self.add_role(server.id, role[0])

    def clear_server_roles(self, server: discord.guild):
        del self.admin_roles[server.id]

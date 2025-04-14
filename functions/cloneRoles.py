from discord.ext import commands
import discord
from ext.utils import Colors

class CloneRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def clone(self, source_guild: discord.Guild, target_guild: discord.Guild):
        await self.clone_roles(source_guild, target_guild)

    async def clone_roles(self, source_guild: discord.Guild, target_guild: discord.Guild):
        await self.delete_all_roles(target_guild)
        
        roles = sorted(source_guild.roles, key=lambda r: r.position)
        roles = [role for role in roles if role.name != "@everyone"]
        
        role_mapping = {}
        
        for role in roles:
            try:
                new_role = await target_guild.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    color=role.color,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                role_mapping[role.id] = new_role
                Colors.success(f"Created role: {role.name}")
            except discord.Forbidden:
                Colors.error(f"No permission to create role: {role.name}")
            except discord.HTTPException as e:
                Colors.error(f"Failed to create role {role.name}: {e}")
        
        positions = {}
        for role in roles:
            if role.id in role_mapping:
                positions[role_mapping[role.id].id] = role.position
        
        if positions:
            try:
                await target_guild.edit_role_positions(positions=positions)
                Colors.success("Role positions updated successfully")
            except discord.Forbidden:
                Colors.error("No permission to edit role positions")
            except discord.HTTPException as e:
                Colors.error(f"Failed to update role positions: {e}")

    async def delete_all_roles(self, guild: discord.Guild):
        roles_to_delete = sorted(
            [role for role in guild.roles if role.name != "@everyone" and role < guild.me.top_role],
            key=lambda r: r.position,
            reverse=True
        )
        
        for role in roles_to_delete:
            try:
                await role.delete()
                Colors.warning(f"Deleted role: {role.name}")
            except discord.Forbidden:
                Colors.error(f"No permission to delete role: {role.name}")
            except discord.HTTPException as e:
                Colors.error(f"Failed to delete role {role.name}: {e}")

def setup(bot):
    bot.add_cog(CloneRoles(bot))

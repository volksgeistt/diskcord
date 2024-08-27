from discord.ext import commands
import discord
from ext.utils import Colors

class CloneGuildConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def clone(self, source_guild: discord.Guild, target_guild: discord.Guild):
        await self.clone_server_settings(source_guild, target_guild)

    async def clone_server_settings(self, source_guild: discord.Guild, target_guild: discord.Guild):
        await target_guild.edit(
            name=source_guild.name,
            verification_level=source_guild.verification_level,
            default_notifications=source_guild.default_notifications,
            explicit_content_filter=source_guild.explicit_content_filter,
            afk_channel=source_guild.afk_channel,
            afk_timeout=source_guild.afk_timeout,
            icon=await source_guild.icon_url.read() if source_guild.icon else None,
        )
        Colors.success("Cloned server settings")

def setup(bot):
    bot.add_cog(CloneGuildConfig(bot))

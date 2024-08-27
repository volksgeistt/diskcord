from discord.ext import commands
import discord
from ext.utils import Colors

class CloneVoiceRegions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def clone(self, source_guild: discord.Guild, target_guild: discord.Guild):
        await self.clone_voice_regions(source_guild, target_guild)

    async def clone_voice_regions(self, source_guild: discord.Guild, target_guild: discord.Guild):
        try:
            await target_guild.edit(region=source_guild.region)
            Colors.success(f"Set voice region to: {source_guild.region}")
        except discord.Forbidden:
            Colors.error("No permission to change voice region")
        except discord.HTTPException as e:
            Colors.error(f"Failed to set voice region: {e}")

def setup(bot):
    bot.add_cog(CloneVoiceRegions(bot))

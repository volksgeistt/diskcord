from discord.ext import commands
import discord
from ext.utils import Colors

class CloneBans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def clone(self, source_guild: discord.Guild, target_guild: discord.Guild):
        await self.clone_bans(source_guild, target_guild)

    async def clone_bans(self, source_guild: discord.Guild, target_guild: discord.Guild):
        try:
            bans = await source_guild.bans()
            for ban_entry in bans:
                try:
                    await target_guild.ban(ban_entry.user, reason=ban_entry.reason)
                    Colors.success(f"Banned user: {ban_entry.user.name}#{ban_entry.user.discriminator}")
                except discord.Forbidden:
                    Colors.error(f"No permission to ban {ban_entry.user.name}#{ban_entry.user.discriminator}")
                except discord.HTTPException as e:
                    Colors.error(f"Failed to ban {ban_entry.user.name}#{ban_entry.user.discriminator}: {e}")
        except discord.Forbidden:
            Colors.error(f"No permission to view bans in the source guild")
        except discord.HTTPException as e:
            Colors.error(f"Failed to retrieve bans from the source guild: {e}")

def setup(bot):
    bot.add_cog(CloneBans(bot))

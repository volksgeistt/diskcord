from discord.ext import commands
import discord
from ext.utils import Colors

class CloneWebhooks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def clone(self, source_guild: discord.Guild, target_guild: discord.Guild):
        await self.clone_webhooks(source_guild, target_guild)

    async def clone_webhooks(self, source_guild: discord.Guild, target_guild: discord.Guild):
        for channel in source_guild.text_channels:
            try:
                webhooks = await channel.webhooks()
                target_channel = discord.utils.get(target_guild.text_channels, name=channel.name)
                
                if target_channel:
                    for webhook in webhooks:
                        avatar = await webhook.avatar.read() if webhook.avatar else None
                        await target_channel.create_webhook(
                            name=webhook.name,
                            avatar=avatar,
                            reason="Cloned from source server"
                        )
                        Colors.success(f"Cloned webhook: {webhook.name} in channel {channel.name}")
                else:
                    Colors.warning(f"Couldn't find matching channel for {channel.name} in target server")
            except discord.Forbidden:
                Colors.error(f"No permission to manage webhooks in {channel.name}")
            except discord.HTTPException as e:
                Colors.error(f"Failed to clone webhooks in {channel.name}: {e}")

def setup(bot):
    bot.add_cog(CloneWebhooks(bot))

from discord.ext import commands
import discord
from ext.utils import Colors

class CloneEmojis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def clone(self, source_guild: discord.Guild, target_guild: discord.Guild):
        await self.clone_emojis(source_guild, target_guild)

    async def clone_emojis(self, source_guild: discord.Guild, target_guild: discord.Guild):
        for emoji in source_guild.emojis:
            try:
                emoji_image = await emoji.url.read()
                await target_guild.create_custom_emoji(name=emoji.name, image=emoji_image)
                Colors.success(f"Created emoji: {emoji.name}")
            except discord.HTTPException:
                Colors.error(f"Failed to create emoji: {emoji.name}")

def setup(bot):
    bot.add_cog(CloneEmojis(bot))

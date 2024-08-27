from discord.ext import commands
import discord
from typing import Optional
from ext.utils import Colors

class CloneChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def clone(self, source_guild: discord.Guild, target_guild: discord.Guild):
        await self.clone_channels(source_guild, target_guild)

    async def clone_channels(self, source_guild: discord.Guild, target_guild: discord.Guild):
        await self.delete_all_channels(target_guild)
        
        for category in source_guild.categories:
            new_category = await target_guild.create_category(category.name)
            for channel in category.channels:
                await self.clone_channel(channel, new_category)

        for channel in source_guild.channels:
            if not channel.category:
                await self.clone_channel(channel, None, target_guild)

    async def clone_channel(self, channel: discord.abc.GuildChannel, category: Optional[discord.CategoryChannel], guild: Optional[discord.Guild] = None):
        if isinstance(channel, discord.TextChannel):
            new_channel = await (guild or category).create_text_channel(
                name=channel.name,
                topic=channel.topic,
                position=channel.position,
                slowmode_delay=channel.slowmode_delay,
                nsfw=channel.nsfw,
                overwrites=channel.overwrites
            )
        elif isinstance(channel, discord.VoiceChannel):
            new_channel = await (guild or category).create_voice_channel(
                name=channel.name,
                bitrate=channel.bitrate,
                user_limit=channel.user_limit,
                position=channel.position,
                overwrites=channel.overwrites
            )
        Colors.success(f"Created channel: {new_channel.name}")

    async def delete_all_channels(self, guild: discord.Guild):
        for channel in guild.channels:
            await channel.delete()
            Colors.warning(f"Deleted channel: {channel.name}")

def setup(bot):
    bot.add_cog(CloneChannels(bot))

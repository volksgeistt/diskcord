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
                await self.clone_channel(channel, new_category, target_guild)

        for channel in source_guild.channels:
            if not channel.category:
                await self.clone_channel(channel, None, target_guild)

    async def clone_channel(self, channel: discord.abc.GuildChannel, category: Optional[discord.CategoryChannel], guild: discord.Guild):
        channel_type = type(channel)
        creation_methods = {
            discord.TextChannel: self.create_text_channel,
            discord.VoiceChannel: self.create_voice_channel,
            discord.StageChannel: self.create_stage_channel,
        }

        create_method = creation_methods.get(channel_type)
        if create_method:
            try:
                new_channel = await create_method(channel, category, guild)
                Colors.success(f"Created {channel_type.__name__}: {new_channel.name}")
            except discord.HTTPException as e:
                Colors.error(f"Failed to create {channel_type.__name__} '{channel.name}': {str(e)}")
        else:
            Colors.warning(f"Unsupported channel type: {channel_type.__name__}")

    async def create_text_channel(self, channel: discord.TextChannel, category: Optional[discord.CategoryChannel], guild: discord.Guild):
        return await guild.create_text_channel(
            name=channel.name,
            topic=channel.topic,
            position=channel.position,
            slowmode_delay=channel.slowmode_delay,
            nsfw=channel.nsfw,
            category=category,
            overwrites=channel.overwrites
        )

    async def create_voice_channel(self, channel: discord.VoiceChannel, category: Optional[discord.CategoryChannel], guild: discord.Guild):
        return await guild.create_voice_channel(
            name=channel.name,
            bitrate=channel.bitrate,
            user_limit=channel.user_limit,
            position=channel.position,
            category=category,
            overwrites=channel.overwrites
        )

    async def create_stage_channel(self, channel: discord.StageChannel, category: Optional[discord.CategoryChannel], guild: discord.Guild):
        return await guild.create_stage_channel(
            name=channel.name,
            topic=channel.topic,
            position=channel.position,
            category=category,
            overwrites=channel.overwrites
        )

    async def delete_all_channels(self, guild: discord.Guild):
        for channel in guild.channels:
            try:
                await channel.delete()
                Colors.warning(f"Deleted channel: {channel.name}")
            except discord.HTTPException as e:
                Colors.error(f"Failed to delete channel '{channel.name}': {str(e)}")

def setup(bot):
    bot.add_cog(CloneChannels(bot))

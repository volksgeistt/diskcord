import asyncio
import os
import discord
from discord.ext import commands
import pyfiglet
from ext.utils import Colors

class ServerCloner(commands.Bot):
    def __init__(self, command_prefix: str, **options):
        super().__init__(command_prefix, **options)
        self.remove_command('help')
        self.cloning_functions = []

    async def on_ready(self):
        Colors.banner(pyfiglet.figlet_format("DiskCord"))
        print(f'[!] : Logged in as {self.user.name}')
        
        await self.load_functions()
        await self.choose_functions()
        await self.clone_server()

    async def load_functions(self):
        for filename in os.listdir('./functions'):
            if filename.endswith('.py'):
                    self.load_extension(f'functions.{filename[:-3]}')

    async def choose_functions(self):
        print("\nLOADED FUNCTIONS:")
        cogs = list(self.cogs.values())
        for i, cog in enumerate(cogs, 1):
            print(f"{i}. {cog.__class__.__name__}")
        print("\n>>> Enter the numbers of the functions you want to use (comma-separated), or 'all' for all modules:")
        choice = input().strip().lower()
        if choice == 'all':
            self.cloning_functions = cogs
        else:
            try:
                choices = [int(x.strip()) for x in choice.split(',')]
                self.cloning_functions = [cogs[i-1] for i in choices if 0 < i <= len(cogs)]
            except ValueError:
                print("[!] INVALID INPUT :- Activating All Functions For Current Target Guild.!")
                self.cloning_functions = cogs

    async def clone_server(self):
        source_guild_id = await self.prompt_for_guild_id("Enter the source guild ID: ")
        target_guild_id = await self.prompt_for_guild_id("Enter the target guild ID: ")

        source_guild = self.get_guild(source_guild_id)
        target_guild = self.get_guild(target_guild_id)

        if not source_guild or not target_guild:
            Colors.error(": Check The Guild IDs, Either One Or Both Of Them Are Invalid.!")
            return

        for cog in self.cloning_functions:
            if hasattr(cog, 'clone'):
                await cog.clone(source_guild, target_guild)

        Colors.success(": TASK COMPLETED : SUCCESSFULLY CLONED")

    async def prompt_for_guild_id(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                Colors.error(": Please Input Valid Guild ID ( Integral Value )")

async def main():
    bot = ServerCloner(command_prefix=".")
    Colors.warning(": Enter Your TOKEN :-  ")
    token = input().strip()
    try:
        await bot.start(token, bot=False)
    except discord.LoginFailure:
        Colors.error(": FAILED! Please Check Your Token!!!")
    except Exception as e:
        Colors.error(f": An error occurred :: {e}")

if __name__ == "__main__":
    asyncio.run(main())

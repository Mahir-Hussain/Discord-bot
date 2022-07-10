import discord
from discord.ext import commands, menus

news = "Resolute is being remastered. Some commands may not function"

class BaseCog(commands.Cog):
    def __init__(self, bot, show_name):
        super().__init__()
        self.bot = bot
        self.show_name = show_name
        colour = 0X00BFFF

class MyPages(menus.MenuPages):

    def __init__(self, source, **kwargs):
        super().__init__(source=source, check_embeds=True, **kwargs)

    async def finalize(self, timed_out):
        try:
            if timed_out:
                await self.message.clear_reactions()
            else:
                await self.message.delete()
        except discord.HTTPException:
            pass


class GroupHelp(menus.ListPageSource):
    """"
    Sends help for group-commands.
    """

    def __init__(self, ctx, group, cmds, *, prefix):
        super().__init__(entries=cmds, per_page=3)
        self.ctx = ctx
        self.group = group
        self.prefix = prefix
        self.title = f"Help for category `{self.group.qualified_name}`"
        self.description = self.group.description

    async def format_page(self, menu, cmds):
        embed = discord.Embed(
            title=self.title,
            description=self.description,
            colour=0X00BFFF
        )
        for cmd in cmds:
            signature = f'{self.prefix}{cmd.qualified_name} {cmd.signature}'
            desc = cmd.help or cmd.brief
            embed.add_field(
                name=signature,
                value=desc.format(prefix=self.ctx.prefix),
                inline=False
            )

        maximum = self.get_max_pages()
        if maximum > 1:
            embed.set_author(
                name=f"Page{menu.current_page + 1} of {maximum} ({len(self.entries)} commands)")
        embed.set_footer(
            text=f"{self.prefix}help to see all commands list.")
        return embed


class MainHelp(menus.ListPageSource):
    """
    Creates an embedded message including all commands
    """

    def __init__(self, ctx, categories: list):
        super().__init__(entries=categories, per_page=6)
        self.ctx = ctx

    async def format_page(self, menu, category):
        embed = discord.Embed(
            title="Help command",
            description=f'\U0001f4f0 **__News__** \n> {news}',
            color=self.ctx.author.colour)
        embed.set_footer(text=f"Use help [command] to get more info.")
        for k, v in category:
            embed.add_field(name=k, value=v, inline=False)

        return embed


class MyHelpCommand(commands.HelpCommand):

    async def get_ending_note(self):
        return f"Type r.{self.invoked_with} Use help [module] for more info on a module. \nUse help [command] for more info on a command."

    async def send_bot_help(self, mapping):
        cats = []
        for cog, cmds in mapping.items():
            if not hasattr(cog, "qualified_name"):
                continue
            name = "No Category" if cog is None else cog.qualified_name + f" [{len(cog.get_commands())}]"
            filtered = await self.filter_commands(cmds, sort=True)
            if filtered:
                all_cmds = " ─ ".join(f"`{c.name}`" for c in cmds)
                if cog:
                    cats.append([name, f">>> {all_cmds}\n"])

        menu = MyPages(source=MainHelp(self.context, cats), timeout=30.0)
        await menu.start(self.context)

    async def send_cog_help(self, cog: BaseCog):
        ctx = self.context
        prefix = "r."
        if not hasattr(cog, "show_name"):
            pass
        entries = await self.filter_commands(cog.get_commands(), sort=True)
        menu = MyPages(
            GroupHelp(ctx, cog, entries, prefix=prefix),
            clear_reactions_after=True,
            timeout=30.0
        )
        await menu.start(ctx)

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=self.get_command_signature(command),
            colour=0X00BFFF
        )
        aliases = " | ".join(command.aliases)
        category = command.cog_name
        if command.aliases:
            embed.add_field(
                name="Aliases",
                value=aliases,
                inline=False
            )
        if category:
            embed.add_field(
                name="Category",
                value="No category..." if not category else category,
                inline=False
            )
        else:
            pass

        if command.description and not command.help:
            embed.description = command.description
        if command.help:
            embed.description = command.help
        else:
            embed.description = command.brief or "No help found..."
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group: commands.Group):
        ctx = self.context
        prefix = "r."
        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)
        entries = await self.filter_commands(subcommands, sort=True)
        if len(entries) == 0:
            return await self.send_command_help(group)
        source = GroupHelp(ctx=ctx, group=group, cmds=entries, prefix=prefix)
        menu = MyPages(source, timeout=30.0)
        await menu.start(ctx)
    
    def get_command_signature(self, command: commands.Command):
        return f"r.{command.qualified_name} {command.signature}"

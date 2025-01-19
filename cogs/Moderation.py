import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        @commands.Cog.listener()
        async def on_ready(self):
            print(f'{self.__class__.__name__} loaded')
    
    @discord.app_commands.command(name='ban', description='ban a member')
    @commands.has_any_role('Administrator', 'Moderator', 'Owner')
    async def ban(self, interaction: discord.Interaction, member: discord.Member,*,reason: str=None):
        if reason is None:
            reason = f'This user is banned by {interaction.user.name}.'
            await member.ban(reason=reason)
            await member.response.send_message(f'{member.display_name} has been banned.')

    @discord.app_commands.command(name='kick', description='kick a member')
    @commands.has_any_role('Administrator', 'Moderator', 'Owner')
    async def kick(self, interaction: discord.Interaction, member: discord.Member,*, reason: str=None):
        if reason is None:
            reason=f'This user is kicked by {interaction.user.name}.'
            await member.kick(reason=reason)
            await interaction.response.send_message(f'{menber.display_name} has been kicked.')

    @discord.app_commands.command(name='mute', description='mute a member for a specified duration')
    @commands.has_any_role('Administrator', 'Moderator', 'Owner')
    async def mute(self, interaction: discord.Interaction, member: discord.Member, timelimit: str):
        if 's' in timelimit:
            seconds = int(timelimit.strip('s'))
            await member.edit(mute=True)
            await interaction.response.send_message(f'{member.display_name} has been muted for {seconds} seconds.')
            await asyncio.sleep(seconds)
            await member.edit(mute=False)
            await interaction.followup.send(f'{member.display_name} has been unmuted.')

    @discord.app_commands.command(name='clear', description='clear a specified number of messages')
    @commands.has_any_role('Administrator', 'Moderator', 'Owner')
    async def clear(self, interaction: discord.Interaction, amount: int=5):
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f'Clear {amount} message.')

    @discord.app_commands.command(name='unmute', description='unmute a member')
    @commands.has_any_role('Administrator', 'Moderator', 'Owner')
    async def unmute(self, interactrion: discord.Interaction, member: discord.Member):
        await member.edit(mute=False)
        await interactrion.response.send_message(f'{member.display_name} has been unmuted.')

    @discord.app_commands.command(name='warn', description='warn a member')
    @commands.has_any_role('Administrator', 'Moderator', 'Owner')
    async def warn(self, interaction: discord.Interaction, member: discord.Member, *, reason: str=None):
        if reason is None:
            await interaction.response.send_message('Please provide a reason for the warning.')
        else:
            await interaction.response.send_message(f'{member.display_name} has been warned for: {reason}.')

    @discord.app_commands.command(name='tempban', description='Temporarily ban a member for a specified duration')
    @commands.has_any_role('Administrator', 'Moderator', 'Owner')
    async def tempban(self, interaction: discord.Interaction, member: discord.Member, duration: str, *, reason: str=None):
        if reason is None:
            await interaction.response.send_message('Please provide a reason for the ban.')
        else:
            await interaction.response.send_message(f'{member.display_name} has been temporarily banned for {duration}.')

    @discord.app_commands.command(name='tempmute', description='Temporarily mute a member for a specified duration')
    @commands.has_any_role('Administrator', 'Moderator', 'Owner')
    async def tempmute(self, interaction: discord.Interaction, member: discord.Member, duration: str,* , reason: str=None):
        if reason is None:
            await interaction.response.send_message('Please provide a reason for the mute')
        else:
            await interaction.response.send_message(f'{member.display_name} has been temporarily muted for {duration}.')

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
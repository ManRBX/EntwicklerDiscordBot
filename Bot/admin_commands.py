import discord
from discord.ext import commands

class AdminCommands(commands.Cog):
    """Eine Sammlung von Admin-Befehlen für den Discord-Bot."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear", aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, amount: int = 10):
        """Löscht eine bestimmte Anzahl von Nachrichten (Standard: 10)."""
        await ctx.channel.purge(limit=amount + 1)  # +1, um den Befehl selbst auch zu löschen
        await ctx.send(f"✅ {amount} Nachrichten wurden gelöscht!", delete_after=3)

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_member(self, ctx, member: discord.Member, *, reason="Kein Grund angegeben"):
        """Kickt ein Mitglied vom Server."""
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} wurde gekickt. Grund: {reason}")

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_member(self, ctx, member: discord.Member, *, reason="Kein Grund angegeben"):
        """Bannt ein Mitglied vom Server."""
        await member.ban(reason=reason)
        await ctx.send(f"⛔ {member.mention} wurde gebannt. Grund: {reason}")

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban_member(self, ctx, *, member_name):
        """Entbannt ein Mitglied anhand des Namens."""
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.name == member_name:
                await ctx.guild.unban(user)
                await ctx.send(f"✅ {user.mention} wurde entbannt!")
                return
        await ctx.send(f"⚠ Kein gebannter Nutzer mit dem Namen {member_name} gefunden.")

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))

import discord
from discord.ext import commands

# ✅ Standardgrund als Konstante definieren, um Duplikate zu vermeiden
DEFAULT_REASON = "Kein Grund angegeben"

class AdminCommands(commands.Cog):
    """Eine Sammlung von Admin-Befehlen für den Discord-Bot."""

    def __init__(self, bot):
        self.bot = bot

    # 🛠 MODERATION
    @commands.command(name="clear", aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, amount: int = 10):
        """Löscht eine bestimmte Anzahl von Nachrichten."""
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"✅ {amount} Nachrichten wurden gelöscht!", delete_after=3)

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_member(self, ctx, member: discord.Member, *, reason=DEFAULT_REASON):
        """Kickt ein Mitglied vom Server."""
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} wurde gekickt. Grund: {reason}")

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_member(self, ctx, member: discord.Member, *, reason=DEFAULT_REASON):
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

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute_member(self, ctx, member: discord.Member, *, reason=DEFAULT_REASON):
        """Stummschaltet einen Benutzer."""
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False)

        await member.add_roles(mute_role)
        await ctx.send(f"🔇 {member.mention} wurde stummgeschaltet. Grund: {reason}")

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute_member(self, ctx, member: discord.Member):
        """Hebt die Stummschaltung eines Benutzers auf."""
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if mute_role:
            await member.remove_roles(mute_role)
            await ctx.send(f"🔊 {member.mention} ist nicht mehr stummgeschaltet.")

    # 🔧 SERVER-VERWALTUNG
    @commands.command(name="set_nickname")
    @commands.has_permissions(manage_nicknames=True)
    async def set_nickname(self, ctx, member: discord.Member, *, nickname):
        """Ändert den Nickname eines Mitglieds."""
        await member.edit(nick=nickname)
        await ctx.send(f"✅ Nickname von {member.mention} wurde zu {nickname} geändert.")

    @commands.command(name="lock_channel")
    @commands.has_permissions(manage_channels=True)
    async def lock_channel(self, ctx):
        """Sperrt den aktuellen Kanal für Nachrichten."""
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Dieser Kanal wurde gesperrt.")

    @commands.command(name="unlock_channel")
    @commands.has_permissions(manage_channels=True)
    async def unlock_channel(self, ctx):
        """Entsperrt den aktuellen Kanal für Nachrichten."""
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 Dieser Kanal wurde entsperrt.")

    @commands.command(name="slowmode")
    @commands.has_permissions(manage_channels=True)
    async def set_slowmode(self, ctx, seconds: int):
        """Setzt den Slowmode für den Kanal."""
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"⏳ Slowmode auf {seconds} Sekunden gesetzt.")

    @commands.command(name="create_role")
    @commands.has_permissions(manage_roles=True)
    async def create_role(self, ctx, *, role_name):
        """Erstellt eine neue Rolle."""
        await ctx.guild.create_role(name=role_name)
        await ctx.send(f"✅ Rolle `{role_name}` wurde erstellt.")

    @commands.command(name="delete_role")
    @commands.has_permissions(manage_roles=True)
    async def delete_role(self, ctx, *, role_name):
        """Löscht eine Rolle."""
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await role.delete()
            await ctx.send(f"❌ Rolle `{role_name}` wurde gelöscht.")
        else:
            await ctx.send(f"⚠ Rolle `{role_name}` nicht gefunden.")

    # 📢 NACHRICHTEN & INTERAKTIONEN
    @commands.command(name="say")
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, message):
        """Lässt den Bot eine Nachricht senden."""
        await ctx.send(message)

    @commands.command(name="poll")
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, question, *options):
        """Erstellt eine Umfrage."""
        if len(options) < 2:
            await ctx.send("⚠ Bitte mindestens zwei Antwortmöglichkeiten angeben.")
            return
        embed = discord.Embed(title=f"📊 Umfrage: {question}", description="\n".join(f"{i+1}. {option}" for i, option in enumerate(options)), color=discord.Color.blue())
        poll_msg = await ctx.send(embed=embed)
        for i in range(len(options)):
            await poll_msg.add_reaction(f"{i+1}️⃣")

    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Fährt den Bot herunter."""
        await ctx.send("🛑 Der Bot wird heruntergefahren...")
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))

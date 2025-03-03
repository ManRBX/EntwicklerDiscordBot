import discord
from discord.ext import commands

class HelpDropdown(discord.ui.Select):
    """Dropdown-Menü für das Hilfe-System."""

    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="📜 Alle Befehle", description="Zeigt alle Befehle", value="all"),
            discord.SelectOption(label="🔧 Admin-Befehle", description="Zeigt nur Admin-Befehle", value="admin"),
            discord.SelectOption(label="ℹ Help-Befehle", description="Zeigt Befehle für das Hilfe-System", value="help"),
        ]
        super().__init__(placeholder="Wähle eine Kategorie...", options=options)

    async def callback(self, interaction: discord.Interaction):
        """Wird ausgeführt, wenn der Benutzer eine Option auswählt."""
        embed = discord.Embed(color=discord.Color.blue())

        if self.values[0] == "all":
            embed.title = "📜 Alle Befehle"
            embed.description = "**Normale Befehle:**\n"
            embed.add_field(name="📢 `!help`", value="Zeigt dieses Hilfe-Menü", inline=False)
            embed.add_field(name="📢 `!echo [Text]`", value="Wiederholt eine Nachricht", inline=False)
            embed.add_field(name="📢 `!info`", value="Zeigt Infos über den Bot", inline=False)

            embed.description += "\n**Admin-Befehle:**\n"
            embed.add_field(name="🔧 `!clear [Anzahl]`", value="Löscht Nachrichten", inline=False)
            embed.add_field(name="🔧 `!kick @Benutzer`", value="Kickt einen Benutzer", inline=False)
            embed.add_field(name="🔧 `!ban @Benutzer`", value="Bannt einen Benutzer", inline=False)
            embed.add_field(name="🔧 `!unban Benutzername`", value="Entbannt einen Benutzer", inline=False)
            embed.add_field(name="🔧 `!mute @Benutzer`", value="Stummschaltet einen Benutzer", inline=False)
            embed.add_field(name="🔧 `!unmute @Benutzer`", value="Hebt die Stummschaltung auf", inline=False)
            embed.add_field(name="🔧 `!poll Frage Option1 Option2 ...`", value="Erstellt eine Umfrage", inline=False)
            embed.add_field(name="🔧 `!set_nickname @Benutzer NeuerName`", value="Ändert den Nickname", inline=False)
            embed.add_field(name="🔧 `!lock_channel`", value="Sperrt den Kanal", inline=False)
            embed.add_field(name="🔧 `!unlock_channel`", value="Entsperrt den Kanal", inline=False)
            embed.add_field(name="🔧 `!create_role Rollenname`", value="Erstellt eine neue Rolle", inline=False)
            embed.add_field(name="🔧 `!delete_role Rollenname`", value="Löscht eine Rolle", inline=False)

        elif self.values[0] == "admin":
            embed.title = "🔧 Admin-Befehle"
            embed.add_field(name="🔧 `!clear [Anzahl]`", value="Löscht Nachrichten", inline=False)
            embed.add_field(name="🔧 `!kick @Benutzer`", value="Kickt einen Benutzer", inline=False)
            embed.add_field(name="🔧 `!ban @Benutzer`", value="Bannt einen Benutzer", inline=False)
            embed.add_field(name="🔧 `!unban Benutzername`", value="Entbannt einen Benutzer", inline=False)
            embed.add_field(name="🔧 `!mute @Benutzer`", value="Stummschaltet einen Benutzer", inline=False)
            embed.add_field(name="🔧 `!unmute @Benutzer`", value="Hebt die Stummschaltung auf", inline=False)
            embed.add_field(name="🔧 `!poll Frage Option1 Option2 ...`", value="Erstellt eine Umfrage", inline=False)
            embed.add_field(name="🔧 `!set_nickname @Benutzer NeuerName`", value="Ändert den Nickname", inline=False)
            embed.add_field(name="🔧 `!lock_channel`", value="Sperrt den Kanal", inline=False)
            embed.add_field(name="🔧 `!unlock_channel`", value="Entsperrt den Kanal", inline=False)
            embed.add_field(name="🔧 `!create_role Rollenname`", value="Erstellt eine neue Rolle", inline=False)
            embed.add_field(name="🔧 `!delete_role Rollenname`", value="Löscht eine Rolle", inline=False)

        elif self.values[0] == "help":
            embed.title = "ℹ Help-Befehle"
            embed.add_field(name="📢 `!help`", value="Zeigt dieses Hilfe-Menü", inline=False)
            embed.add_field(name="📢 `!info`", value="Zeigt Infos über den Bot", inline=False)

        embed.set_footer(text="Wähle eine andere Kategorie im Dropdown-Menü!")
        await interaction.response.edit_message(embed=embed, view=self.view)


class HelpView(discord.ui.View):
    """Erstellt die Dropdown-Ansicht für das Help-Menü."""
    def __init__(self, bot):
        super().__init__()
        self.add_item(HelpDropdown(bot))


class HelpCommand(commands.Cog):
    """Help-Befehl mit Dropdown-Menü"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Sendet das Dropdown-Help-Menü"""
        embed = discord.Embed(title="📜 Hilfe-Menü", description="Wähle eine Kategorie aus dem Dropdown-Menü!", color=discord.Color.green())
        await ctx.send(embed=embed, view=HelpView(self.bot))


async def setup(bot):
    await bot.add_cog(HelpCommand(bot))

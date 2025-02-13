import discord
from discord.ext import commands

class HelpDropdown(discord.ui.Select):
    """Dropdown-Menü für das Hilfe-System."""

    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="🔹 Alle Befehle", description="Zeigt alle verfügbaren Befehle", value="all"),
            discord.SelectOption(label="🔧 Admin-Befehle", description="Zeigt nur Admin-Befehle", value="admin"),
        ]
        super().__init__(placeholder="Wähle eine Kategorie...", options=options)

    async def callback(self, interaction: discord.Interaction):
        """Wird ausgeführt, wenn der Benutzer eine Option auswählt."""
        if self.values[0] == "all":
            embed = discord.Embed(title="📜 Alle Befehle", color=discord.Color.blue())
            embed.add_field(name="🔹 `!help`", value="Zeigt dieses Hilfe-Menü", inline=False)
            embed.add_field(name="🔹 `!echo [Text]`", value="Wiederholt eine Nachricht", inline=False)
            embed.add_field(name="🔹 `!info`", value="Zeigt Infos über den Bot", inline=False)
            embed.add_field(name="🔧 `!clear [Anzahl]`", value="Löscht Nachrichten (Admin)", inline=False)
            embed.add_field(name="🔧 `!kick @Benutzer`", value="Kickt einen Benutzer (Admin)", inline=False)
            embed.add_field(name="🔧 `!ban @Benutzer`", value="Bannt einen Benutzer (Admin)", inline=False)
            embed.set_footer(text="Nutze /help für weitere Infos")
        
        elif self.values[0] == "admin":
            embed = discord.Embed(title="🔧 Admin-Befehle", color=discord.Color.red())
            embed.add_field(name="🔧 `!clear [Anzahl]`", value="Löscht Nachrichten", inline=False)
            embed.add_field(name="🔧 `!kick @Benutzer`", value="Kickt einen Benutzer", inline=False)
            embed.add_field(name="🔧 `!ban @Benutzer`", value="Bannt einen Benutzer", inline=False)
            embed.add_field(name="🔧 `!unban Benutzername`", value="Entbannt einen Benutzer", inline=False)
            embed.set_footer(text="Nur Admins können diese Befehle ausführen!")

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

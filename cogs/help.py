"""
Help Commands Cog
Provides help and setup commands for the bot
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="help", description="Display all available commands")
    @app_commands.describe(category="Choose a specific category to view")
    @app_commands.choices(category=[
        app_commands.Choice(name="🎮 Gaming", value="gaming"),
        app_commands.Choice(name="🏆 Tournament", value="tournament"),
        app_commands.Choice(name="💰 Economy", value="economy"),
        app_commands.Choice(name="🔧 Utility", value="utility"),
        app_commands.Choice(name="📚 Study", value="study"),
        app_commands.Choice(name="🛡️ Moderation", value="moderation"),
        app_commands.Choice(name="🎉 Fun", value="fun"),
        app_commands.Choice(name="📊 Stats", value="stats"),
    ])
    async def help_command(self, interaction: discord.Interaction, category: Optional[str] = None):
        """Display help information for bot commands"""
        
        if category is None:
            # Main help menu
            embed = discord.Embed(
                title="🤖 MegaBot Help Menu",
                description="Welcome to MegaBot! Here are all available command categories.\nUse `/help category:<name>` to see commands in a specific category.",
                color=discord.Color.blue()
            )
            
            categories = {
                "🎮 Gaming": "Steam profiles, LFG system, game deals, gaming roles",
                "🏆 Tournament": "Create and manage tournaments with brackets",
                "💰 Economy": "Virtual currency, shop, gambling games, leaderboards",
                "🔧 Utility": "Polls, reminders, translate, calculator, server info",
                "📚 Study": "Pomodoro timer, homework tracker, quiz system",
                "🛡️ Moderation": "Kick, ban, mute, clear, slowmode, warnings, giveaways",
                "🎉 Fun": "Jokes, memes, 8ball, trivia, dice, fortune",
                "📊 Stats": "Server stats, channel stats, top chatters, emoji stats"
            }
            
            for cat_name, description in categories.items():
                embed.add_field(
                    name=cat_name,
                    value=description,
                    inline=False
                )
            
            embed.add_field(
                name="💡 Quick Start",
                value="Try `/balance` to start your economy journey!\nUse `/giveaway` to run server giveaways!\nTry `/pomodoro` to start studying!",
                inline=False
            )
            
            embed.set_footer(text=f"Total Commands: 58 | Requested by {interaction.user.display_name}")
            
        else:
            # Category-specific help
            commands_dict = {
                "gaming": {
                    "title": "🎮 Gaming Commands",
                    "commands": [
                        "/steam <profile> - View Steam profile information",
                        "/playing - See what server members are currently playing",
                        "/lfg <game> <players> - Create a looking-for-group post",
                        "/gamedeal <game> - Search for game deals and discounts",
                        "/gamerole <game> - Get a gaming role for a specific game"
                    ]
                },
                "tournament": {
                    "title": "🏆 Tournament Commands",
                    "commands": [
                        "/createtournament - Create a new tournament",
                        "/jointournament - Join an active tournament",
                        "/leavetournament - Leave a tournament you joined",
                        "/tournamentinfo - View detailed tournament information",
                        "/starttournament - Start the tournament (organizer only)",
                        "/listtournaments - List all active tournaments",
                        "/deletetournament - Delete a tournament (organizer only)"
                    ]
                },
                "economy": {
                    "title": "💰 Economy Commands",
                    "commands": [
                        "/balance - Check your current balance and active boosts",
                        "/daily - Claim your daily reward (24h cooldown)",
                        "/work - Work to earn money",
                        "/transfer <user> <amount> - Transfer money to another user",
                        "/leaderboard - View the richest users on the server",
                        "/shop - View items available in the shop",
                        "/buy <item> - Buy an item from the shop",
                        "/inventory - View your items and boosts",
                        "/use <item> - Activate a consumable item",
                        "/sell <item> <quantity> - Sell items for money",
                        "/rob <user> - Attempt to rob another user",
                        "/slots <bet> - Play the slot machine",
                        "/blackjack <bet> - Play blackjack game"
                    ]
                },
                "utility": {
                    "title": "🔧 Utility Commands",
                    "commands": [
                        "/poll <question> <options> - Create a poll",
                        "/remind <time> <message> - Set a reminder",
                        "/translate <text> <language> - Translate text to another language",
                        "/calculate <expression> - Calculate math expressions",
                        "/userinfo <user> - Get detailed information about a user",
                        "/serverinfo - Get server information and statistics",
                        "/avatar <user> - View and download user's avatar"
                    ]
                },
                "study": {
                    "title": "📚 Study Commands",
                    "commands": [
                        "/pomodoro - Start a 25-minute Pomodoro study timer",
                        "/stoppomodoro - Stop your active Pomodoro timer",
                        "/homework add - Add a new homework assignment",
                        "/homeworklist - View all your homework assignments",
                        "/homeworkdone - Mark a homework assignment as complete",
                        "/homeworkdelete - Delete a homework assignment",
                        "/quiz - Take a quick trivia quiz to test your knowledge"
                    ]
                },
                "moderation": {
                    "title": "🛡️ Moderation Commands",
                    "commands": [
                        "/kick <member> <reason> - Kick a member from the server",
                        "/ban <member> <reason> - Ban a member from the server",
                        "/mute <member> <duration> - Temporarily mute a member",
                        "/unmute <member> - Remove mute from a member",
                        "/warn <member> <reason> - Warn a member",
                        "/clear <amount> - Clear specified number of messages",
                        "/slowmode <seconds> - Set channel slowmode delay",
                        "/setwelcome <channel> - Set welcome message channel",
                        "/setautorole <role> - Set auto-role for new members",
                        "/removeautorole - Remove auto-role",
                        "/giveaway <duration> <prize> - Start a giveaway"
                    ]
                },
                "fun": {
                    "title": "🎉 Fun Commands",
                    "commands": [
                        "/joke - Get a random joke",
                        "/meme - Get a random meme from Reddit",
                        "/8ball <question> - Ask the magic 8-ball a question",
                        "/trivia - Start a trivia game with multiple questions",
                        "/flip - Flip a coin (heads or tails)",
                        "/roll <dice> - Roll dice (e.g., 2d6 for two 6-sided dice)",
                        "/choose <options> - Let the bot choose between options",
                        "/fortune - Get your fortune told",
                        "/rate <thing> - Rate something out of 10"
                    ]
                },
                "stats": {
                    "title": "📊 Stats Commands",
                    "commands": [
                        "/serverstats - View comprehensive server statistics",
                        "/channelstats <channel> - View specific channel statistics",
                        "/roleinfo <role> - View detailed role information",
                        "/topchatters - View most active chatters in the server",
                        "/emojistats - View emoji usage statistics",
                        "/membercount - View member count growth over time"
                    ]
                }
            }
            
            if category in commands_dict:
                cat_data = commands_dict[category]
                embed = discord.Embed(
                    title=cat_data["title"],
                    description=f"Here are all commands in the {category} category:",
                    color=discord.Color.green()
                )
                
                for cmd in cat_data["commands"]:
                    embed.add_field(
                        name=cmd.split(" - ")[0],
                        value=cmd.split(" - ")[1] if " - " in cmd else "No description",
                        inline=False
                    )
                
                embed.set_footer(text=f"Use /help to see all categories | Requested by {interaction.user.display_name}")
            else:
                embed = discord.Embed(
                    title="❌ Invalid Category",
                    description="Please select a valid category from the dropdown!",
                    color=discord.Color.red()
                )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="setup", description="Setup the bot for your server")
    @app_commands.default_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        """Setup wizard for the bot"""
        
        embed = discord.Embed(
            title="🔧 MegaBot Setup Wizard",
            description="Welcome to MegaBot setup! Follow these steps to configure the bot:",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="1️⃣ Create Channels",
            value="Create these optional channels:\n"
                  "• `#mod-logs` - For moderation logs\n"
                  "• `#welcome` - For welcome messages\n"
                  "• `#economy` - For economy commands\n"
                  "• `#gaming` - For LFG posts",
            inline=False
        )
        
        embed.add_field(
            name="2️⃣ Set Permissions",
            value="Make sure the bot has these permissions:\n"
                  "✅ Manage Messages\n"
                  "✅ Manage Roles\n"
                  "✅ Kick Members\n"
                  "✅ Ban Members\n"
                  "✅ Send Messages\n"
                  "✅ Embed Links",
            inline=False
        )
        
        embed.add_field(
            name="3️⃣ Configure Moderation",
            value="Use these commands to set up moderation:\n"
                  "• `/slowmode` - Set channel slowmode\n"
                  "• `/lock` - Lock channels when needed",
            inline=False
        )
        
        embed.add_field(
            name="4️⃣ Economy Setup",
            value="The economy system is ready to use!\n"
                  "Users can start with `/balance` and `/daily`",
            inline=False
        )
        
        embed.add_field(
            name="5️⃣ Test Commands",
            value="Try these commands to test:\n"
                  "• `/help` - View all commands\n"
                  "• `/serverinfo` - View server info\n"
                  "• `/poll` - Create a test poll",
            inline=False
        )
        
        embed.add_field(
            name="✅ You're All Set!",
            value="Your bot is now configured! Use `/help` to see all available commands.\n"
                  "Need help? Check the documentation or contact support.",
            inline=False
        )
        
        embed.set_footer(text=f"Setup by {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="info", description="Get information about the bot")
    async def info(self, interaction: discord.Interaction):
        """Display bot information"""
        
        embed = discord.Embed(
            title="ℹ️ About MegaBot",
            description="A comprehensive Discord bot with economy, gaming, sports, utility tools, and more!",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📊 Statistics",
            value=f"Servers: {len(self.bot.guilds)}\n"
                  f"Users: {sum(g.member_count for g in self.bot.guilds)}\n"
                  f"Commands: 66",
            inline=True
        )
        
        embed.add_field(
            name="🔧 Features",
            value="• 💰 Economy System\n"
                  "• 🎮 Gaming Integration\n"
                  "• ⚽ Sports Betting\n"
                  "• 📚 Study Tools\n"
                  "• 🛡️ Moderation Tools",
            inline=True
        )
        
        embed.add_field(
            name="🔗 Links",
            value="[Discord Developer Portal](https://discord.com/developers/applications/)",
            inline=False
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"MegaBot v1.0 | Requested by {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="dashboard", description="Get the link to the web dashboard")
    async def dashboard(self, interaction: discord.Interaction):
        """Provides link to the web dashboard"""
        
        embed = discord.Embed(
            title="🌐 MegaBot Web Dashboard",
            description="Access the interactive web dashboard to explore all bot features, commands, and statistics!",
            color=discord.Color.blurple()
        )
        
        embed.add_field(
            name="📊 Dashboard Features",
            value="• 📋 Complete command list with details\n"
                  "• 📈 Real-time bot statistics\n"
                  "• 🎮 Feature overview and categories\n"
                  "• 📱 Responsive mobile-friendly design\n"
                  "• 🔍 Interactive command explorer",
            inline=False
        )
        
        embed.add_field(
            name="🔗 Access Dashboard",
            value="**[Click here to open dashboard](https://megabotdiscord.netlify.app/)**",
            inline=False
        )
        
        embed.add_field(
            name="💡 Tip",
            value="Bookmark the dashboard for quick access to command documentation and bot stats!",
            inline=False
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")
        
        # Create a button for easy access
        view = discord.ui.View()
        button = discord.ui.Button(
            label="Open Dashboard",
            style=discord.ButtonStyle.link,
            url="https://megabotdiscord.netlify.app/",
            emoji="🌐"
        )
        view.add_item(button)
        
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Help(bot))

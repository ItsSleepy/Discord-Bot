import discord
from discord import app_commands
from discord.ext import commands
from config import Config
import logging

logger = logging.getLogger('MegaBot.Admin')

# Admin user ID
ADMIN_ID = 546429809459200000

def is_admin():
    """Check if user is the bot admin"""
    def predicate(interaction: discord.Interaction) -> bool:
        return interaction.user.id == ADMIN_ID
    return app_commands.check(predicate)

class Admin(commands.Cog):
    """Admin commands for bot owner only"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="adminpanel", description="[ADMIN ONLY] View admin panel")
    @is_admin()
    async def adminpanel(self, interaction: discord.Interaction):
        """Display admin panel with available commands"""
        embed = discord.Embed(
            title="🔐 Admin Panel",
            description="Bot Administration Commands",
            color=0xFF0000
        )
        
        embed.add_field(
            name="💰 Economy Management",
            value=(
                "`/setbalance <user> <amount>` - Set user's balance\n"
                "`/addbalance <user> <amount>` - Add money to user\n"
                "`/removebalance <user> <amount>` - Remove money from user\n"
                "`/resetbalance <user>` - Reset user's balance to starting amount"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🎒 Inventory Management",
            value=(
                "`/giveitem <user> <item> <quantity>` - Give item to user\n"
                "`/removeitem <user> <item> <quantity>` - Remove item from user\n"
                "`/clearinventory <user>` - Clear user's entire inventory\n"
                "`/viewinventory <user>` - View any user's inventory"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🔄 Boost Management",
            value=(
                "`/giveboost <user> <boost> <hours>` - Give active boost to user\n"
                "`/removeboost <user> <boost>` - Remove specific boost from user\n"
                "`/clearboosts <user>` - Clear all boosts from user"
            ),
            inline=False
        )
        
        embed.add_field(
            name="📊 Data Management",
            value=(
                "`/viewuserdata <user>` - View complete user data\n"
                "`/resetuser <user>` - Complete user data reset\n"
                "`/backup` - Create database backup (Coming soon)"
            ),
            inline=False
        )
        
        embed.set_footer(text=f"Admin: {interaction.user.name} • Only you can see this")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="setbalance", description="[ADMIN ONLY] Set a user's balance")
    @app_commands.describe(user="User to modify", amount="New balance amount")
    @is_admin()
    async def setbalance(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        """Set user's balance to specific amount"""
        guild_id = interaction.guild.id if interaction.guild else 0
        
        if amount < 0:
            await interaction.response.send_message(
                f"{Config.EMOJI_ERROR} Amount cannot be negative!",
                ephemeral=True
            )
            return
        
        # Get current balance
        current_balance = await self.bot.db.get_balance(user.id, guild_id)
        
        # Calculate difference and update
        difference = amount - current_balance
        await self.bot.db.update_balance(user.id, difference, guild_id)
        
        embed = discord.Embed(
            title="✅ Balance Updated",
            description=f"Successfully set **{user.display_name}**'s balance",
            color=Config.COLOR_SUCCESS
        )
        embed.add_field(name="Previous Balance", value=f"${current_balance:,}", inline=True)
        embed.add_field(name="New Balance", value=f"${amount:,}", inline=True)
        embed.set_footer(text=f"Admin: {interaction.user.name}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"Admin {interaction.user.name} set {user.name}'s balance to ${amount}")
    
    @app_commands.command(name="addbalance", description="[ADMIN ONLY] Add money to a user")
    @app_commands.describe(user="User to give money to", amount="Amount to add")
    @is_admin()
    async def addbalance(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        """Add money to user's balance"""
        guild_id = interaction.guild.id if interaction.guild else 0
        
        if amount <= 0:
            await interaction.response.send_message(
                f"{Config.EMOJI_ERROR} Amount must be positive!",
                ephemeral=True
            )
            return
        
        current_balance = await self.bot.db.get_balance(user.id, guild_id)
        new_balance = await self.bot.db.update_balance(user.id, amount, guild_id)
        
        embed = discord.Embed(
            title="✅ Money Added",
            description=f"Added **${amount:,}** to **{user.display_name}**",
            color=Config.COLOR_SUCCESS
        )
        embed.add_field(name="Previous Balance", value=f"${current_balance:,}", inline=True)
        embed.add_field(name="New Balance", value=f"${new_balance:,}", inline=True)
        embed.set_footer(text=f"Admin: {interaction.user.name}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"Admin {interaction.user.name} added ${amount} to {user.name}")
    
    @app_commands.command(name="removebalance", description="[ADMIN ONLY] Remove money from a user")
    @app_commands.describe(user="User to remove money from", amount="Amount to remove")
    @is_admin()
    async def removebalance(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        """Remove money from user's balance"""
        guild_id = interaction.guild.id if interaction.guild else 0
        
        if amount <= 0:
            await interaction.response.send_message(
                f"{Config.EMOJI_ERROR} Amount must be positive!",
                ephemeral=True
            )
            return
        
        current_balance = await self.bot.db.get_balance(user.id, guild_id)
        new_balance = await self.bot.db.update_balance(user.id, -amount, guild_id)
        
        embed = discord.Embed(
            title="✅ Money Removed",
            description=f"Removed **${amount:,}** from **{user.display_name}**",
            color=Config.COLOR_SUCCESS
        )
        embed.add_field(name="Previous Balance", value=f"${current_balance:,}", inline=True)
        embed.add_field(name="New Balance", value=f"${new_balance:,}", inline=True)
        embed.set_footer(text=f"Admin: {interaction.user.name}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"Admin {interaction.user.name} removed ${amount} from {user.name}")
    
    @app_commands.command(name="resetbalance", description="[ADMIN ONLY] Reset user's balance to starting amount")
    @app_commands.describe(user="User to reset")
    @is_admin()
    async def resetbalance(self, interaction: discord.Interaction, user: discord.Member):
        """Reset user's balance to starting amount (1000)"""
        guild_id = interaction.guild.id if interaction.guild else 0
        
        current_balance = await self.bot.db.get_balance(user.id, guild_id)
        difference = 1000 - current_balance
        await self.bot.db.update_balance(user.id, difference, guild_id)
        
        embed = discord.Embed(
            title="✅ Balance Reset",
            description=f"Reset **{user.display_name}**'s balance to starting amount",
            color=Config.COLOR_SUCCESS
        )
        embed.add_field(name="Previous Balance", value=f"${current_balance:,}", inline=True)
        embed.add_field(name="New Balance", value=f"$1,000", inline=True)
        embed.set_footer(text=f"Admin: {interaction.user.name}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"Admin {interaction.user.name} reset {user.name}'s balance")
    
    @app_commands.command(name="giveitem", description="[ADMIN ONLY] Give an item to a user")
    @app_commands.describe(user="User to give item to", item="Item name", quantity="Amount to give")
    @is_admin()
    async def giveitem(self, interaction: discord.Interaction, user: discord.Member, item: str, quantity: int = 1):
        """Give item to user's inventory"""
        guild_id = interaction.guild.id if interaction.guild else 0
        
        if quantity <= 0:
            await interaction.response.send_message(
                f"{Config.EMOJI_ERROR} Quantity must be positive!",
                ephemeral=True
            )
            return
        
        item_lower = item.lower().replace(' ', '_')
        
        # Define item types
        item_types = {
            "padlock": "security",
            "alarm_system": "security",
            "guard_dog": "security",
            "lockpick": "tool",
            "reverse_rob_card": "security",
            "lucky_charm": "consumable",
            "briefcase": "consumable",
            "energy_drink": "consumable",
            "diamond_multiplier": "consumable",
            "loaded_dice": "consumable"
        }
        
        item_type = item_types.get(item_lower, "tool")
        
        # Add to inventory
        await self.bot.db.add_inventory_item(user.id, guild_id, item_lower, item_type, quantity)
        
        embed = discord.Embed(
            title="✅ Item Given",
            description=f"Gave **{quantity}x {item.replace('_', ' ').title()}** to **{user.display_name}**",
            color=Config.COLOR_SUCCESS
        )
        embed.add_field(name="Item Type", value=item_type.title(), inline=True)
        embed.add_field(name="Quantity", value=str(quantity), inline=True)
        embed.set_footer(text=f"Admin: {interaction.user.name}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"Admin {interaction.user.name} gave {quantity}x {item} to {user.name}")
    
    @app_commands.command(name="removeitem", description="[ADMIN ONLY] Remove an item from a user")
    @app_commands.describe(user="User to remove item from", item="Item name", quantity="Amount to remove")
    @is_admin()
    async def removeitem(self, interaction: discord.Interaction, user: discord.Member, item: str, quantity: int = 1):
        """Remove item from user's inventory"""
        guild_id = interaction.guild.id if interaction.guild else 0
        
        if quantity <= 0:
            await interaction.response.send_message(
                f"{Config.EMOJI_ERROR} Quantity must be positive!",
                ephemeral=True
            )
            return
        
        item_lower = item.lower().replace(' ', '_')
        
        # Check if user has the item
        current_qty = await self.bot.db.get_item_quantity(user.id, guild_id, item_lower)
        if current_qty < quantity:
            await interaction.response.send_message(
                f"{Config.EMOJI_ERROR} {user.display_name} only has {current_qty}x {item}!",
                ephemeral=True
            )
            return
        
        # Remove from inventory
        success = await self.bot.db.use_inventory_item(user.id, guild_id, item_lower, quantity)
        
        if success:
            embed = discord.Embed(
                title="✅ Item Removed",
                description=f"Removed **{quantity}x {item.replace('_', ' ').title()}** from **{user.display_name}**",
                color=Config.COLOR_SUCCESS
            )
            embed.add_field(name="Previous Quantity", value=str(current_qty), inline=True)
            embed.add_field(name="New Quantity", value=str(current_qty - quantity), inline=True)
            embed.set_footer(text=f"Admin: {interaction.user.name}")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logger.info(f"Admin {interaction.user.name} removed {quantity}x {item} from {user.name}")
        else:
            await interaction.response.send_message(
                f"{Config.EMOJI_ERROR} Failed to remove item!",
                ephemeral=True
            )
    
    @app_commands.command(name="clearinventory", description="[ADMIN ONLY] Clear user's entire inventory")
    @app_commands.describe(user="User to clear inventory")
    @is_admin()
    async def clearinventory(self, interaction: discord.Interaction, user: discord.Member):
        """Clear user's entire inventory"""
        guild_id = interaction.guild.id if interaction.guild else 0
        
        # Get current inventory
        items = await self.bot.db.get_inventory(user.id, guild_id)
        item_count = len(items)
        
        # Clear all items
        for item in items:
            await self.bot.db.remove_inventory_item(user.id, guild_id, item['item_name'])
        
        embed = discord.Embed(
            title="✅ Inventory Cleared",
            description=f"Cleared **{user.display_name}**'s entire inventory",
            color=Config.COLOR_SUCCESS
        )
        embed.add_field(name="Items Removed", value=str(item_count), inline=True)
        embed.set_footer(text=f"Admin: {interaction.user.name}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"Admin {interaction.user.name} cleared {user.name}'s inventory")
    
    @app_commands.command(name="viewinventory", description="[ADMIN ONLY] View any user's inventory")
    @app_commands.describe(user="User to view")
    @is_admin()
    async def viewinventory(self, interaction: discord.Interaction, user: discord.Member):
        """View any user's inventory"""
        guild_id = interaction.guild.id if interaction.guild else 0
        
        items = await self.bot.db.get_inventory(user.id, guild_id)
        
        embed = discord.Embed(
            title=f"🔍 Admin View: {user.display_name}'s Inventory",
            color=0xFF0000
        )
        
        if not items:
            embed.description = "Inventory is empty."
        else:
            # Group by item type
            security_items = [item for item in items if item['item_type'] == 'security']
            consumables = [item for item in items if item['item_type'] == 'consumable']
            tools = [item for item in items if item['item_type'] == 'tool']
            
            if security_items:
                security_text = []
                for item in security_items:
                    name = item['item_name'].replace('_', ' ').title()
                    security_text.append(f"🛡️ **{name}** x{item['quantity']}")
                embed.add_field(name="🔒 Security Items", value="\n".join(security_text), inline=False)
            
            if tools:
                tool_text = []
                for item in tools:
                    name = item['item_name'].replace('_', ' ').title()
                    tool_text.append(f"🔧 **{name}** x{item['quantity']}")
                embed.add_field(name="🛠️ Tools", value="\n".join(tool_text), inline=False)
            
            if consumables:
                consumable_text = []
                for item in consumables:
                    name = item['item_name'].replace('_', ' ').title()
                    consumable_text.append(f"✨ **{name}** x{item['quantity']}")
                embed.add_field(name="💊 Consumables", value="\n".join(consumable_text), inline=False)
        
        embed.set_footer(text=f"Admin: {interaction.user.name}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="viewuserdata", description="[ADMIN ONLY] View complete user data")
    @app_commands.describe(user="User to view")
    @is_admin()
    async def viewuserdata(self, interaction: discord.Interaction, user: discord.Member):
        """View complete user data"""
        guild_id = interaction.guild.id if interaction.guild else 0
        
        # Get balance
        balance = await self.bot.db.get_balance(user.id, guild_id)
        
        # Get inventory
        items = await self.bot.db.get_inventory(user.id, guild_id)
        
        # Get active boosts
        boosts = await self.bot.db.get_active_boosts(user.id, guild_id)
        
        # Get rob stats
        rob_stats = await self.bot.db.get_rob_stats(user.id, guild_id)
        
        embed = discord.Embed(
            title=f"🔍 Complete User Data: {user.display_name}",
            color=0xFF0000
        )
        
        embed.add_field(name="💰 Balance", value=f"${balance:,}", inline=True)
        embed.add_field(name="🎒 Items", value=str(len(items)), inline=True)
        embed.add_field(name="✨ Active Boosts", value=str(len(boosts)), inline=True)
        
        embed.add_field(
            name="📊 Rob Statistics",
            value=f"Total Attempts: {rob_stats['total_attempts']}\n"
                  f"Successful: {rob_stats['successful']}\n"
                  f"Failed: {rob_stats['failed']}\n"
                  f"Times Robbed: {rob_stats['times_robbed']}",
            inline=False
        )
        
        if items:
            item_list = [f"{item['item_name'].replace('_', ' ').title()} x{item['quantity']}" for item in items[:10]]
            if len(items) > 10:
                item_list.append(f"... and {len(items) - 10} more")
            embed.add_field(name="🎒 Inventory Items", value="\n".join(item_list), inline=False)
        
        embed.set_footer(text=f"Admin: {interaction.user.name} • User ID: {user.id}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="resetuser", description="[ADMIN ONLY] Complete user data reset")
    @app_commands.describe(user="User to reset", confirm="Type 'CONFIRM' to proceed")
    @is_admin()
    async def resetuser(self, interaction: discord.Interaction, user: discord.Member, confirm: str):
        """Complete user data reset"""
        if confirm != "CONFIRM":
            await interaction.response.send_message(
                f"{Config.EMOJI_ERROR} Please type 'CONFIRM' to proceed with full reset!",
                ephemeral=True
            )
            return
        
        guild_id = interaction.guild.id if interaction.guild else 0
        
        # Reset balance to starting amount
        current_balance = await self.bot.db.get_balance(user.id, guild_id)
        difference = 1000 - current_balance
        await self.bot.db.update_balance(user.id, difference, guild_id)
        
        # Clear inventory
        items = await self.bot.db.get_inventory(user.id, guild_id)
        for item in items:
            await self.bot.db.remove_inventory_item(user.id, guild_id, item['item_name'])
        
        # Clear boosts (handled automatically by expiry)
        
        embed = discord.Embed(
            title="✅ User Reset Complete",
            description=f"Completely reset **{user.display_name}**'s data",
            color=Config.COLOR_SUCCESS
        )
        embed.add_field(name="Balance", value="Reset to $1,000", inline=True)
        embed.add_field(name="Inventory", value=f"Cleared {len(items)} items", inline=True)
        embed.add_field(name="⚠️ Warning", value="This action cannot be undone!", inline=False)
        embed.set_footer(text=f"Admin: {interaction.user.name}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.warning(f"Admin {interaction.user.name} performed full reset on {user.name}")
    
    @adminpanel.error
    @setbalance.error
    @addbalance.error
    @removebalance.error
    @resetbalance.error
    @giveitem.error
    @removeitem.error
    @clearinventory.error
    @viewinventory.error
    @viewuserdata.error
    @resetuser.error
    async def admin_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Handle admin command errors"""
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message(
                f"{Config.EMOJI_ERROR} You don't have permission to use this command! This is an admin-only command.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"{Config.EMOJI_ERROR} An error occurred: {str(error)}",
                ephemeral=True
            )
            logger.error(f"Admin command error: {error}")

async def setup(bot):
    await bot.add_cog(Admin(bot))
    logger.info("Admin cog loaded")

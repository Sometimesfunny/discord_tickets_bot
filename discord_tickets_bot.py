from discord import app_commands, Interaction, Client, Color, Embed, Intents, TextChannel, File, errors
from utils.utils import *
from tickets.buttons_views import *
import os

ticket_processor = TicketProcessor.from_dict(load_data('tickets_data.json'))
TicketMenuView.ticket_processor = ticket_processor
CloseButtonView.ticket_processor = ticket_processor

class DiscordBot(Client):
    def __init__(self, *args, **kwargs):
        intents = Intents.default()
        intents.message_content = True
        super().__init__(intents=intents, *args, **kwargs)
        self.synced = False

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        if not self.synced:
            await tree.sync()
            self.synced = True
        if ticket_processor.ticket_menu_message_id is not None:
            try:
                channel = await self.fetch_channel(ticket_processor.ticket_menu_channel_id)
                message = await channel.fetch_message(ticket_processor.ticket_menu_message_id)
                await message.edit(view=TicketMenuView())
            except errors.NotFound:
                print("Ticket menu message not found in on_ready")
        for ticket in ticket_processor.opened_tickets:
            try:
                channel = await self.fetch_channel(ticket.channel_id)
                message = await channel.fetch_message(ticket.first_message_id)
                await message.edit(view=CloseButtonView())
            except errors.NotFound:
                ticket_processor.close_ticket(ticket.ticket_id, 'Channel deleted while bot was offline')
                save_data('tickets_data.json', ticket_processor.to_dict())
                print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} Ticket #{ticket.ticket_id} closed because the channel or the first message was deleted")
        print("Ready! Synced")
        print("------")

bot = DiscordBot(command_prefix="!")

@bot.event
async def on_guild_channel_delete(channel):
    if not isinstance(channel, TextChannel):
        return
    channel : TextChannel = channel
    ticket = ticket_processor.get_ticket_by_channel_id(channel.id)
    if ticket is None:
        return
    ticket_processor.close_ticket(ticket, 'Channel deleted')
    print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} Ticket #{ticket.ticket_id} closed without saving message history")

tree = app_commands.CommandTree(bot)

# command to create a ticket menu
@tree.command(name="ticket_menu")
async def ticket_menu(interaction : Interaction, create_in_category : bool = True):
    if not interaction.user.guild_permissions.administrator:
        return
    if ticket_processor.ticket_menu_message_id is not None:
        try:
            channel = await interaction.guild.fetch_channel(ticket_processor.ticket_menu_channel_id)
            message = await channel.fetch_message(ticket_processor.ticket_menu_message_id)
            await message.delete()
        except errors.NotFound:
            print("Ticket menu message not found in ticket_menu")
    category = None
    if ticket_processor.tickets_category_id is None:
        category = await interaction.guild.create_category("Tickets")
        await category.set_permissions(interaction.guild.default_role, read_messages=False)
        ticket_processor.tickets_category_id = category.id
    embed = Embed(
        title="Ticket Menu", 
        description="Please select a ticket type", 
        color=Color.blurple()
        )
    embed.set_thumbnail(url='https://drive.google.com/uc?export=view&id=1E6sLAVevWmUdFiJ05gj4LHaVC_lNMXbn')
    embed.add_field(name="Open Ticket", value="Push this button if you have any question/proposal about DBS DAO", inline=False)
    embed.add_field(name="Collaboration", value="Push this button if you want to offer a collaboration", inline=False)
    view = TicketMenuView()
    if create_in_category:
        if category is None:
            category = await interaction.guild.fetch_channel(ticket_processor.tickets_category_id)
        if ticket_processor.ticket_menu_channel_id is None:
            channel = await category.create_text_channel("🎫open-ticket")
        else:
            try:
                channel = await interaction.guild.fetch_channel(ticket_processor.ticket_menu_channel_id)
            except errors.NotFound:
                print("Ticket menu channel not found in ticket_menu, creating new one")
                channel = await category.create_text_channel("🎫open-ticket")
        message = await channel.send(embed=embed, view=view)
    else:
        message = await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message('Ticket Menu created', ephemeral=True)
    ticket_processor.ticket_menu_channel_id = message.channel.id
    ticket_processor.ticket_menu_message_id = message.id
    save_data('tickets_data.json', ticket_processor.to_dict())

@tree.command(name="get_ticket_log")
async def get_ticket_log(interaction : Interaction, ticket_id : int):
    if not interaction.user.guild_permissions.administrator:
        return
    ticket_message_history = ticket_processor.get_ticket_message_history(ticket_id)
    if ticket_message_history is None:
        await interaction.response.send_message("Ticket not found", ephemeral=True)
        return
    with open(f"{ticket_id}.txt", "w") as f:
        f.write(ticket_message_history)
    await interaction.response.send_message(ephemeral=True, file=File(f"{ticket_id}.txt"))
    os.remove(f"{ticket_id}.txt")

token = load_token('discord_tickets_config.ini')

bot.run(token)

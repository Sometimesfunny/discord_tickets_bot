from datetime import datetime
from discord.ui import View, button, Button
from discord import Interaction, ButtonStyle, Embed
from .ticket_processor import TicketProcessor
from .modals_classes import NormalTicketModal, CollaborativeTicketModal
from utils.utils import save_data

class TicketMenuView(View):

    ticket_processor : TicketProcessor = None

    def __init__(self):
        super().__init__(timeout=None)
        if self.ticket_processor is None:
            raise ValueError("TicketProcessor not set")
    
    async def prepare_ticket(self, ticket_type : str, interaction : Interaction):
        ticket = self.ticket_processor.get_ticket_by_user_id_and_type(interaction.user.id, ticket_type)
        if ticket is not None:
            await interaction.response.send_message(f"You already have an opened ticket <#{ticket.channel_id}>", ephemeral=True)
            return
        if ticket_type == 'normal':
            modal_view = NormalTicketModal()
            ticket_name = 'ticket'
        elif ticket_type == 'collab':
            modal_view = CollaborativeTicketModal()
            ticket_name = 'collab'
        await interaction.response.send_modal(modal_view)
        if await modal_view.wait():
            return
        new_ticket = self.ticket_processor.open_ticket(interaction.user.id, ticket_type, modal_view.answer.value)
        if self.ticket_processor.tickets_category_id is None:
            new_channel = await interaction.guild.create_text_channel(
                f"{ticket_name}-{new_ticket.ticket_id}",
                topic=f"Ticket opened by {interaction.user.name}#{interaction.user.discriminator}"
                )
        else:
            category = await interaction.guild.fetch_channel(self.ticket_processor.tickets_category_id)
            new_channel = await category.create_text_channel(
                f"{ticket_name}-{new_ticket.ticket_id}",
                topic=f"Ticket opened by {interaction.user.name}#{interaction.user.discriminator}"
                )
        await new_channel.set_permissions(interaction.guild.default_role, read_messages=False)
        await new_channel.set_permissions(interaction.guild.get_role(1010587178574827550), read_messages=False)
        await new_channel.set_permissions(interaction.guild.get_role(1009828332994580491), read_messages=True)
        await new_channel.set_permissions(interaction.user, read_messages=True, send_messages=True, read_message_history=True)
        embed = Embed(
            title=f"Ticket #{new_ticket.ticket_id}",
            description=f"Opened by {interaction.user.mention}",
            color=0x00ff00
        )
        embed.add_field(name="Reason", value=modal_view.answer.value)
        first_message = await new_channel.send(embed=embed, content="@everyone", view=CloseButtonView())
        new_ticket.channel_id = new_channel.id
        new_ticket.first_message_id = first_message.id
        print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} {new_ticket.ticket_type} Ticket #{new_ticket.ticket_id} opened by {interaction.user.name}#{interaction.user.discriminator}")
        save_data('tickets_data.json', self.ticket_processor.to_dict())
        await interaction.followup.send(f"Ticket opened {new_channel.mention}", ephemeral=True)

    @button(label="Open Ticket", style=ButtonStyle.green, custom_id="open_ticket")
    async def open_ticket(self, interaction: Interaction, button : Button):
        await self.prepare_ticket("normal", interaction)

    @button(label="Collaboration", style=ButtonStyle.blurple, custom_id="collab")
    async def open_collab_ticket(self, interaction: Interaction, button : Button):
        await self.prepare_ticket("collab", interaction)
        
class CloseButtonView(View):

    ticket_processor : TicketProcessor = None

    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Close Ticket", style=ButtonStyle.red, custom_id="close_ticket")
    async def close_ticket(self, interaction: Interaction, button : Button):
        ticket = self.ticket_processor.get_ticket_by_channel_id(interaction.channel.id)
        if ticket is None:
            await interaction.response.send_message("This channel is not a ticket", ephemeral=True)
            return
        embed = Embed(
            title=f"Ticket #{ticket.ticket_id}",
            description=f"Closed by {interaction.user.mention}",
            color=0xff0000
        )
        await interaction.response.edit_message(embed=embed, view=None)
        message_history = ''
        user = await interaction.guild.fetch_member(ticket.user_id)
        await interaction.channel.set_permissions(target=user, send_messages=False)
        if ticket.ticket_type == 'normal':
            await interaction.channel.edit(name=f"closed-{ticket.ticket_id}")
        elif ticket.ticket_type == 'collab':
            await interaction.channel.edit(name=f"closed-col-{ticket.ticket_id}")
        messages_list = []
        async for message in interaction.channel.history(limit=None):
            one_message = f"{message.author.name}#{message.author.discriminator}:\n"
            if message.content != '':
                one_message += f'Content:\n{message.content}\n'
            if len(message.attachments) > 0:
                one_message += f"Attachments:\n{[attachment.url for attachment in message.attachments]}\n"
            one_message += '\n'
            messages_list.append(one_message)
        messages_list.reverse()
        message_history = f'{"-"*20}\nTicket #{ticket.ticket_id}\nOpened: {ticket.open_date}\nClosed: {ticket.close_date}\nReason: {ticket.reason}\nUser id: {ticket.user_id}\nTicket type: {ticket.ticket_type}\n{"-"*20}\n\n\n'
        message_history += ''.join(messages_list)
        self.ticket_processor.close_ticket(ticket, message_history)
        save_data('tickets_data.json', self.ticket_processor.to_dict())
        print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} {ticket.ticket_type} Ticket #{ticket.ticket_id} closed by {interaction.user.name}#{interaction.user.discriminator}")

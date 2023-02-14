from discord.ui import Modal, TextInput
from discord import TextStyle, Interaction

class NormalTicketModal(Modal, title="Ticket"):

    def __init__(self):
        super().__init__(timeout=300)

    answer = TextInput(
        label="Write your question/proposal here",
        placeholder="Why do you want to open a ticket?",
        style=TextStyle.long
    )

    async def on_submit(self, interaction : Interaction):
        await interaction.response.edit_message(content=None)

class CollaborativeTicketModal(Modal, title="Collaborative Ticket"):

    def __init__(self):
        super().__init__(timeout=300)

    answer = TextInput(
        label="Write your collaboration proposal here",
        placeholder="Why do you want to open a collaborative ticket?",
        style=TextStyle.long
    )

    async def on_submit(self, interaction : Interaction):
        await interaction.response.edit_message(content=None)
    


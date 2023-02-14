from .ticket import Ticket
from typing import Union
from utils.utils import save_data
class TicketProcessor():

    @staticmethod
    def from_dict(data : dict):
        if 'current_ticket_id' in data:
            Ticket.current_ticket_id = int(data['current_ticket_id'])
        if 'opened_tickets' in data:
            return TicketProcessor([Ticket.from_dict(ticket) for ticket in data['opened_tickets']], [Ticket.from_dict(ticket) for ticket in data['closed_tickets']], data['tickets_category_id'], data['ticket_menu_channel_id'], data['ticket_menu_message_id'])
        else:
            return TicketProcessor()

    def __init__(self, opened_tickets : list = [], closed_tickets : list = [], tickets_category_id : int = None, ticket_menu_channel_id : int = None, ticket_menu_message_id : int = None) -> None:
        self.opened_tickets = opened_tickets
        self.closed_tickets = closed_tickets
        self.tickets_category_id = tickets_category_id
        self.ticket_menu_channel_id = ticket_menu_channel_id
        self.ticket_menu_message_id = ticket_menu_message_id
    
    def set_ticket_menu_channel_id(self, channel_id : int):
        self.ticket_menu_channel_id = channel_id
    
    def set_ticket_menu_message_id(self, message_id : int):
        self.ticket_menu_message_id = message_id
    
    def set_tickets_category_id(self, category_id : int):
        self.tickets_category_id = category_id
        save_data('tickets_data.json', self.to_dict())
    
    def set_ticket_menu(self, channel_id : int, message_id : int):
        self.ticket_menu_channel_id = channel_id
        self.ticket_menu_message_id = message_id
        save_data('tickets_data.json', self.to_dict())

    def open_ticket(self, user_id : int, ticket_type : str, reason : str):
        ticket = Ticket(user_id, ticket_type, reason)
        self.opened_tickets.append(ticket)
        return ticket
    
    def get_closed_ticket_by_id(self, ticket_id : int):
        for ticket in self.closed_tickets:
            if ticket.ticket_id == ticket_id:
                return ticket
        return None
    
    def get_ticket_by_id(self, ticket_id : int):
        for ticket in self.opened_tickets:
            if ticket.ticket_id == ticket_id:
                return ticket
        return None
    
    def get_ticket_by_channel_id(self, channel_id : int):
        for ticket in self.opened_tickets:
            if ticket.channel_id == channel_id:
                return ticket
        return None
    
    def get_ticket_by_user_id(self, user_id : int):
        for ticket in self.opened_tickets:
            if ticket.user_id == user_id:
                return ticket
        return None
    
    def close_ticket(self, ticket : Union[int, Ticket], message_history : str):
        if isinstance(ticket, int):
            ticket = self.get_ticket_by_id(ticket)
        ticket.close_ticket(message_history)
        self.opened_tickets.remove(ticket)
        self.closed_tickets.append(ticket)
    
    def to_dict(self):
        return {
            "current_ticket_id": Ticket.current_ticket_id,
            "tickets_category_id": self.tickets_category_id,
            "ticket_menu_channel_id": self.ticket_menu_channel_id,
            "ticket_menu_message_id": self.ticket_menu_message_id,
            "opened_tickets": [ticket.to_dict() for ticket in self.opened_tickets],
            "closed_tickets": [ticket.to_dict() for ticket in self.closed_tickets]
        }
    
    def get_ticket_by_user_id_and_type(self, user_id : int, ticket_type : str):
        for ticket in self.opened_tickets:
            if ticket.user_id == user_id and ticket.ticket_type == ticket_type:
                return ticket
        return None
    
    def get_ticket_message_history(self, ticket : Union[int, Ticket]):
        if isinstance(ticket, int):
            ticket = self.get_closed_ticket_by_id(ticket)
            if ticket is None:
                return None
        return ticket.get_message_history()

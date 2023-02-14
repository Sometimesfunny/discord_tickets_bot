import datetime
class Ticket():
    current_ticket_id = 0

    @staticmethod
    def get_next_ticket_id():
        Ticket.current_ticket_id += 1
        return Ticket.current_ticket_id
    
    @staticmethod
    def from_dict(data : dict):
        return Ticket(
            data['user_id'], 
            data['ticket_type'], 
            data['reason'], 
            data['ticket_id'], 
            data['channel_id'], 
            data['ticket_status'], 
            data['message_history'], 
            data['open_date'], 
            data['close_date'],
            data['first_message_id']
            )
    
    def __init__(self, 
        user_id : int, 
        ticket_type : str, 
        reason : str, 
        ticket_id : int =None, 
        channel_id : int =None, 
        ticket_status : str="opened", 
        message_history : str="", 
        open_date : str=None,
        close_date : str=None,
        first_message_id : int=None
        ) -> None:
        self.user_id = user_id
        self.ticket_type = ticket_type
        self.reason = reason
        if ticket_id is None:
            self.ticket_id = self.get_next_ticket_id()
        else:
            self.ticket_id = ticket_id
        
        self.channel_id = channel_id
        self.ticket_status = ticket_status
        self.message_history = message_history.replace('\\n', '\n')
        if open_date is None:
            self.open_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        else:
            self.open_date = open_date
        
        if close_date is None:
            self.close_date = None
        else:
            self.close_date = close_date
        
        self.first_message_id : int = first_message_id
    
    def close_ticket(self, message_history : str):
        self.ticket_status = "closed"
        self.message_history = message_history
        self.close_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "ticket_type": self.ticket_type,
            "reason": self.reason,
            "ticket_id": self.ticket_id,
            "channel_id": self.channel_id,
            "ticket_status": self.ticket_status,
            "message_history": self.message_history,
            "open_date": self.open_date,
            "close_date": self.close_date,
            "first_message_id": self.first_message_id
        }
    
    def set_channel_id(self, channel_id : int):
        self.channel_id = channel_id
    
    def open_ticket(self):
        self.ticket_status = "open"
    
    def add_message(self, message : str):
        self.message_history += f"{message}"
    
    def get_message_history(self):
        return self.message_history
        
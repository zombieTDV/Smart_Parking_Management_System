from config.setting import settings
from src.models.parking_slot import parking_slot#, transaction_repo
# from src.models import Transaction

class CarOwner:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        
        
        self.fee = 0.0

    def view_available_slots(self):
        """
        Hiển thị danh sách các chỗ đỗ.
        """
        parking_slot.view_available_slots()

    
    
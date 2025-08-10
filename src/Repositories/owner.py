from config.setting import settings
from src.models.parking_slot import parking_slot#, transaction_repo
# from src.models import Transaction

class CarOwner:
    def __init__(self) -> None:
        pass

    def view_available_slots(self):
        """
        Hiển thị danh sách các chỗ đỗ.
        """
        parking_slot.view_available_slots()

    
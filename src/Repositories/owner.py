from config.setting import settings
from src.models.parking_slot import parking_slot#, transaction_repo
# from src.models import Transaction

class CarOwner:
    def __init__(self) -> None:
        pass

    def view_available_slots(self):
        """
        Hiển thị danh sách các chỗ đỗ còn trống.
        """
        free_slots = parking_slot.get_available_slots()
        if not free_slots:
            print("❌ Hiện tại không có chỗ trống.")
            return

        print("\nChỗ đỗ còn trống:")
        for slot in free_slots:
            print(f"- ID: {slot[0]}") # type: ignore
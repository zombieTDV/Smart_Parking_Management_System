from src.services.parking_service import view_available_slots, check_in_vehicle, check_out_vehicle
from src.models.transaction import transaction_service
class ParkingAttendant:
    def __init__(self):
        pass
    
    def view_available_slots(self):
        """
        Hiển thị danh sách các chỗ đỗ còn trống.
        """
        view_available_slots()
    
    def check_in_vehicle(self, user_id: int, slot_id: int, username: str):
        """
        Xử lý check-in cho xe vào bãi đỗ.
        """
        check_in_vehicle(user_id, slot_id, username)
        
    def check_out_vehicle(self, user_id: int, slot_id: int):
        """
        Xử lý check-out cho xe ra khỏi bãi đỗ.
        """
        check_out_vehicle(user_id, slot_id)
        
    
    def view_transaction_history(self):
        """
        Hiển thị lịch sử giao dịch.
        """
        transaction_service.view_all_records()
        
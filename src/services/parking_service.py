from src.services.fee_calculator import fee_calculator
from src.models.transaction import transaction_service, TransactionRecord
from src.models.parking_slot import parking_slot
from config.setting import settings

def calculate_fee(ID: int, slot_id: int) -> float:
    total = fee_calculator(transaction_service.get_duration_seconds(ID, slot_id))
    return total

def view_available_slots() -> None:
    """
    In danh sách các slot còn trống.
    """
    parking_slot.view_available_slots()

def check_in_vehicle(slot_id: int, username: str) -> None:
    """
    Xử lý check-in cho xe vào bãi đỗ.
    """
    if not parking_slot.is_slot_available(slot_id):
        print(f"❌ Chỗ đỗ ID {slot_id} không còn trống.")
        return
    else:
        parking_slot.table.set_value(
            record_name='slot_id',
            record_id=slot_id,
            column='available',
            value=False
        )
        user = TransactionRecord(slot_id, username)
        user.check_in_user()
        parking_slot.set_slot_status(slot_id, False)
        
        
        print(f"✅ Xe của người dùng {username} đã được check-in vào chỗ đỗ ID {slot_id}.")
        
        
def find_user_id_by_username(username: str) -> int:
    """
    Tìm ID người dùng dựa trên tên đăng nhập.
    """
    ID = transaction_service.find_user_by_username(username)
    return ID if ID else -1

def find_slot_id_by_user_id(username: str) -> int:
    """
    Tìm ID chỗ đỗ dựa trên ID người dùng.
    """
    slot_id = transaction_service.find_slot_by_username(username)
    return slot_id if slot_id else -1

def check_out_vehicle(ID: int, slot_id: int) -> None:
    """
    Xử lý check-out cho xe ra khỏi bãi đỗ.
    """
    transaction_service.check_out_vehicle(ID, slot_id) 
    fee = calculate_fee(ID, slot_id)
    print(f"Số tiền thanh toán: {fee} VND")
    
    settings.day_p += fee
    settings.save()
    
from config.setting import settings
from src.models.parking_slot import parking_slot
from src.models.account import accounts_central
class ADMIN():
    def __init__(self) -> None:
        pass
        
        
    def set_total_slots(self, total_slots: int) -> None:
        """
        Cập nhật tổng số chỗ đỗ.
        """
        if total_slots <= 0:
            parking_slot.delete_all_slots()
        else:
            parking_slot.set_total_slots(total_slots)
            parking_slot.modifile_slots()
    
    def set_hourly_rates(self, hourly_rates: float) -> None:
        """
        Cập nhật giá theo giờ.
        """
        parking_slot.set_hourly_rates(hourly_rates)
    
    def view_available_slots(self) -> None:
        """
        In danh sách các slot còn trống.
        """
        parking_slot.view_available_slots()
        
    def view_all_accounts(self) -> None:
        """
        Hiển thị tất cả tài khoản đã đăng ký.
        """
        accounts_central.view_all_accounts()
        
    def delete_all_accounts(self) -> None:
        """
        Xóa tất cả tài khoản đã đăng ký.
        """
        accounts_central.delete_all_accounts()
        
    
    
    
admin = ADMIN()


from config.setting import settings
from src.models.parking_slot import Parking_slot
from src.models.account import accounts_central
class ADMIN():
    def __init__(self) -> None:
        self.parking_slot = Parking_slot(
            total_slots=settings.cfg["parking_slot"]["total_slots"],
            hourly_rates=settings.cfg["parking_slot"]["hourly_rates"])
        
        
    def set_total_slots(self, total_slots: int) -> None:
        """
        Cập nhật tổng số chỗ đỗ.
        """
        self.parking_slot.set_total_slots(total_slots)
        self.parking_slot.modifile_slots()
    
    def set_hourly_rates(self, hourly_rates: float) -> None:
        """
        Cập nhật giá theo giờ.
        """
        self.parking_slot.set_hourly_rates(hourly_rates)
    
    def view_available_slots(self) -> None:
        """
        In danh sách các slot còn trống.
        """
        self.parking_slot.view_available_slots()
        
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


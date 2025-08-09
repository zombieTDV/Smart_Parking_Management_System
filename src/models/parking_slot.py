from config.setting import settings
from src.database import Table, db
from datetime import datetime

class Parking_slot:
    def __init__(self, total_slots=None, hourly_rates=None):
        self.table = Table("parking_slot", db)
        self.table.create("slot_id INT AUTO_INCREMENT PRIMARY KEY, available BOOL NOT NULL")
        
        if total_slots is None:
            total_slots = settings.cfg["parking_slot"]["total_slots"]
        if hourly_rates is None:
            hourly_rates = settings.cfg["parking_slot"]["hourly_rates"]
        # Lấy rate và tổng slot từ cấu hình
        self.total_slots = total_slots
        self.hourly_rates = hourly_rates
        
        
        settings.cfg["parking_slot"]["total_slots"] = total_slots
        settings.cfg["parking_slot"]["hourly_rates"] = hourly_rates
        settings.save()
        
        self.set_up_parking_slots(self.total_slots) # type: ignore
        # self.update_from_settings()
        
    def __repr__(self):
        return f"Parking_slot(total_slots={self.total_slots}, hourly_rates={self.hourly_rates})"
    
    def set_total_slots(self, total_slots: int) -> None:
        """
        Cập nhật tổng số chỗ đỗ.
        """
        settings.cfg["parking_slot"]["total_slots"] = total_slots
        settings.save()
        
        self.update_from_settings()
        
    def set_hourly_rates(self, hourly_rates: float) -> None:
        """
        Cập nhật giá theo giờ.
        """
        settings.cfg["parking_slot"]["hourly_rates"] = hourly_rates
        settings.save()
        
        self.update_from_settings()
        
    def update_from_settings(self):
        """
        Cập nhật thông tin từ cấu hình.
        """
        self.total_slots = settings.cfg["parking_slot"]["total_slots"]
        self.hourly_rates = settings.cfg["parking_slot"]["hourly_rates"]
        
    def set_up_parking_slots(self, size: int) -> None:
        """
        Tạo bảng `parking_slot` và chèn các slot theo tổng số.
        """
        self.table.create("slot_id INT AUTO_INCREMENT PRIMARY KEY, available BOOL NOT NULL")

        if self.table.count() == 0: # type: ignore
            for _ in range(size):
                self.table.insert(["available"], (True,))
    
    def modifile_slots(self) -> None:    
        """
        Chèn các slot vào bảng.
        """ 
        if self.table.count() < self.total_slots: # type: ignore
            for slot in range(self.total_slots - self.table.count()): # type: ignore
                # Chèn slot vào bảng
                self.table.insert(["available"], (True,))
        elif self.table.count() > self.total_slots: # type: ignore
            slot_id = self.table.count()
            for _ in range(self.table.count() - self.total_slots): # type: ignore
                self.table.delete(record_name='slot_id', record_id=slot_id) # type: ignore
                slot_id -= 1
        else:
            print("Slot size are not modfiled.")

        
    def view_available_slots(self) -> None:
        select = self.table.select_all()
        print("=== Parking Status ===")
        for i in range(self.table.count()):
            if select[i][1] == 1: # type: ignore
                print(f"ID: {select[i][0]}  ----- availability: Free") # type: ignore
            else:
                print(f"ID: {select[i][0]}  ----- availability: Occupied") # type: ignore
                
        
parking_slot = Table("parking_slot", db)

            
    
from config.setting import settings
from src.database import parking_slot
class ADMIN():
    def __init__(self) -> None:
        pass 
    
    #Configure parking lot settings 
    def set_total_slots(self, total_slots: int) -> None:        
        settings.cfg["parking_slot"]["total_slots"]= total_slots
        settings.save()
        
    def set_hourly_rates(self, hourly_rates: float) -> None:
        settings.cfg["parking_slot"]["hourly_rates"]= hourly_rates
        settings.save()
    
    
    def manage_parking_slots(self) -> None:
        select = parking_slot.select_all()
        print("=== Parking Status ===")
        for i in range(parking_slot.count()):
            if select[i][1] == 1: # type: ignore
                print(f"ID: {select[i][0]}  ----- availability: Free") # type: ignore
            else:
                print(f"ID: {select[i][0]}  ----- availability: Occupied") # type: ignore
    
    def configure_parking_lot(self) -> None:
        print("\n--- Cấu hình bãi đỗ ---")
        total_slots = int(input("Nhập tổng số chỗ đỗ: "))
        hourly_rates = float(input("Nhập giá theo giờ: "))
        
        self.set_total_slots(total_slots)
        self.set_hourly_rates(hourly_rates)
        
    def generate_revenue_report(self) -> None:
        print("\n--- Báo cáo doanh thu ---")
        total_revenue = settings.cfg["parking_slot"]["total_slots"] * settings.cfg["parking_slot"]["hourly_rates"]
        print(f"Tổng doanh thu dự kiến: {total_revenue} VND")
        
admin = ADMIN()

# src/repositories/admin.py
from database import SessionLocal
from src.models.parking_slot import ParkingSlot

class AdminRepo:
    def __init__(self):
        self.db = SessionLocal()

    def set_rate(self, rate: float):
        # lưu config tạm vào file hoặc bảng config (đơn giản: file .env)
        # tại đây ta giả lập ghi ra console
        print(f"[Repo] Cập nhật rate: {rate}")

    def configure_slots(self, total: int):
        # xóa hết và tạo mới
        self.db.query(ParkingSlot).delete()
        for i in range(1, total + 1):
            slot = ParkingSlot(id=i)
            self.db.add(slot)
        self.db.commit()

    def add_slot(self):
        last = self.db.query(ParkingSlot).order_by(ParkingSlot.id.desc()).first()
        new_id = last.id + 1 if last else 1
        slot = ParkingSlot(id=new_id)
        self.db.add(slot)
        self.db.commit()
        return slot.id

    def update_slot(self, slot_id: int, occupied: bool):
        slot = self.db.query(ParkingSlot).get(slot_id)
        if slot:
            slot.is_occupied = occupied
            self.db.commit()
            return True
        return False

    def delete_slot(self, slot_id: int):
        res = self.db.query(ParkingSlot).filter_by(id=slot_id).delete()
        self.db.commit()
        return bool(res)
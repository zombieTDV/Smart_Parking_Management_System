from datetime import datetime
from config.setting import settings
from src.database import Table, db
from src.models.parking_slot import parking_slot  

class ParkingAttendant:
    def __init__(self):
        self.rate_per_hour = settings.cfg["parking_slot"]["hourly_rates"]

    def view_available_slots(self) -> None:
        """
        In danh sách các slot còn trống.
        """
        parking_slot.view_available_slots()

    # def check_in_vehicle(self, plate_number):

    #     available_slots = self.view_available_slots()
    #     if not available_slots:
    #         return

    #     assigned_slot = available_slots[0]
    #     check_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #     # Đánh dấu slot là occupied
    #     self.slots_table.set_value(
    #         record_name='slot_id',
    #         record_id=assigned_slot,
    #         column='available',
    #         value=False
    #     )

    #     # Thêm xe vào bảng vehicles
    #     self.vehicles_table.insert(
    #         ["plate_number", "slot_id", "check_in"],
    #         (plate_number, assigned_slot, check_in_time)
    #     )

    #     print(f"Vehicle {plate_number} checked in at slot {assigned_slot}.")

    # def check_out_vehicle(self, plate_number):
    #     """Trả xe, tính phí, lưu giao dịch"""
    #     row = self.vehicles_table.find_record_with_value(column="plate_number", value=plate_number)
    #     if not row:
    #         print("Vehicle not found.")
    #         return

    #     slot = row[0][1]   # slot_id ở cột thứ 2 (0: id, 1: slot_id, 2: check_in)
    #     check_in_str = row[0][2]
    #     check_in_time = datetime.strptime(check_in_str, "%Y-%m-%d %H:%M:%S")

    #     duration = datetime.now() - check_in_time
    #     hours_parked = int(duration.total_seconds() // 3600)
    #     if duration.total_seconds() % 3600 > 0:
    #         hours_parked += 1

    #     fee = hours_parked * self.rate_per_hour
    #     check_out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #     # Giải phóng chỗ
    #     self.slots_table.set_value(
    #         record_name='slot_id',
    #         record_id=slot,
    #         column='available',
    #         value=True
    #     )

    #     # Xóa xe khỏi bảng vehicles
    #     self.vehicles_table.delete(record_name='plate_number', record_id=plate_number)

    #     # Lưu giao dịch
    #     self.transactions_table.insert(
    #         ["plate_number", "slot_id", "check_in", "check_out", "fee"],
    #         (plate_number, slot, check_in_str, check_out_time, fee)
    #     )

    #     print(f"Vehicle {plate_number} checked out from slot {slot}.")
    #     print(f"Hours parked: {hours_parked}, Fee: ${fee}")

    # def view_transactions(self):
    #     """Xem toàn bộ lịch sử giao dịch"""
    #     records = self.transactions_table.select_all()
    #     if not records:
    #         print("No transactions found.")
    #         return
    #     print("\nTransaction History:")
    #     for record in records:
    #         # Giả sử cột: id, plate_number, slot_id, check_in, check_out, fee
    #         print(f"Plate: {record[1]} | Slot: {record[2]} | In: {record[3]} | Out: {record[4]} | Fee: ${record[5]}")


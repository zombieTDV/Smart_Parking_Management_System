# from config.setting import settings
# from src.database import parking_slot, parking_vehicle
# from datetime import datetime

# class ParkingAttendant:
#     def __init__(self):
#         # Lấy rate và tổng slot từ cấu hình
#         self.rate_per_hour = settings.cfg["parking_slot"]["hourly_rates"]
#         self.total_slots   = settings.cfg["parking_slot"]["total_slots"]

#         # Đảm bảo các bảng đã được tạo và khởi dữ liệu
#         self._ensure_slot_table()
#         self._ensure_vehicle_table()

#     def _ensure_slot_table(self) -> None:
#         """
#         Tạo bảng `parking_slot` và chèn các slot theo tổng số.
#         """
#         parking_slot.create(
#             "slot_id INT AUTO_INCREMENT PRIMARY KEY, "
#             "available BOOL NOT NULL"
#         )
#         if parking_slot.count() == 0:
#             for _ in range(self.total_slots):
#                 parking_slot.insert(["available"], (True,))

#     def _ensure_vehicle_table(self) -> None:
#         """
#         Tạo bảng `parking_vehicle` để ghi lịch sử gửi xe.
#         """
#         parking_vehicle.create(
#             "record_id INT AUTO_INCREMENT PRIMARY KEY, "
#             "plate_number VARCHAR(20) NOT NULL, "
#             "slot_id INT NOT NULL, "
#             "check_in DATETIME NOT NULL"
#         )

#     def view_available_slots(self) -> None:
#         """
#         In danh sách các slot còn trống.
#         """
#         rows      = parking_slot.select_all()
#         free_ids  = [row[0] for row in rows if row[1]] # type: ignore
#         print("Available Slots:", free_ids)

#     def check_in_vehicle(self, plate_number: str) -> None:
#         """
#         Gán slot đầu tiên rảnh cho xe, đánh dấu occupied,
#         và lưu bản ghi gửi xe vào table `parking_vehicle`.
#         """
#         rows = parking_slot.select_all()
#         free = [r for r in rows if r[1]] # type: ignore
#         if not free:
#             print("No available slots right now.")
#             return

#         slot_id = free[0][0] # type: ignore
#         # Cập nhật slot
#         parking_slot.update(slot_id, {"available": False})
#         # Chèn record xe
#         now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         parking_vehicle.insert(
#             ["plate_number", "slot_id", "check_in"],
#             (plate_number, slot_id, now)
#         )
#         print(f"Vehicle {plate_number} checked in at slot {slot_id}.")

#     def check_out_vehicle(self, plate_number: str) -> None:
#         """
#         Tìm record xe, tính phí, giải phóng slot, xóa record.
#         """
#         # Lấy tất cả bản ghi và tìm xe
#         records = parking_vehicle.select_all()
#         rec = next(
#             (r for r in records if r[1] == plate_number),
#             None
#         )
#         if not rec:
#             print("Vehicle not found.")
#             return

#         record_id, _, slot_id, check_in_str = rec
#         check_in = datetime.strptime(check_in_str, "%Y-%m-%d %H:%M:%S")

#         # Tính số giờ (làm tròn lên)
#         delta   = datetime.now() - check_in
#         hours   = int(delta.total_seconds() // 3600)
#         if delta.total_seconds() % 3600:
#             hours += 1

#         fee = hours * self.rate_per_hour

#         # Giải phóng slot và xóa bản ghi
#         parking_slot.update(slot_id, {"available": True})
#         parking_vehicle.delete(record_id)

#         print(f"Vehicle {plate_number} checked out from slot {slot_id}.")
#         print(f"Hours parked: {hours}, Fee: ${fee}")


# Khởi tạo attendant
attendant = ParkingAttendant()

from config.setting import settings
from src.database import parking_slot, transaction_repo
from src.models import ParkingSlot, Transaction

class ATTENDANT:
    def __init__(self) -> None:
        pass

    def check_in_vehicle(self):
        """
        Nhận xe vào bãi, gán chỗ đỗ và tạo giao dịch mới.
        """
        plate = input("Nhập biển số xe: ").strip().upper()
        free_slots = parking_slot.get_available_slots()
        if not free_slots:
            print("❌ Hiện tại không còn chỗ trống.")
            return

        print("\nDanh sách chỗ đỗ trống:")
        for slot in free_slots:
            print(f"- ID: {slot.id} | Vị trí: {slot.location or 'N/A'}")

        slot_id = input("\nChọn ID chỗ đỗ: ").strip()
        try:
            parking_slot.assign_vehicle_to_slot(slot_id, plate)
            transaction_repo.create_transaction(plate, slot_id)
            print(f"✅ Xe {plate} đã được gán vào chỗ {slot_id}.")
        except Exception as e:
            print(f"❌ Lỗi khi check-in: {e}")

    def check_out_vehicle(self):
        """
        Xuất xe, tính phí dựa trên thời gian sử dụng và đóng giao dịch.
        """
        plate = input("Nhập biển số xe cần xuất: ").strip().upper()
        tr = transaction_repo.get_active_transaction_by_plate(plate)
        if not tr:
            print("❌ Không tìm thấy giao dịch đang mở cho xe này.")
            return

        hours = tr.calculate_duration_hours()
        fee   = hours * settings.hourly_rate
        print(f"\nThời gian đỗ: {hours} giờ")
        print(f"Phí phải thanh toán: {fee} $")

        confirm = input("Xác nhận thanh toán? (y/n): ").strip().lower()
        if confirm == 'y':
            transaction_repo.close_transaction(tr.id, fee)
            parking_slot.release_slot(tr.slot_id)
            print("✅ Thanh toán thành công. Xe đã được xuất.")
        else:
            print("❌ Đã hủy thao tác check-out.")

    def update_slot_status(self):
        """
        Cập nhật thủ công trạng thái (free/occupied) của một chỗ đỗ.
        """
        slot_id = input("Nhập ID chỗ đỗ: ").strip()
        status  = input("Trạng thái (0: Trống, 1: Đang sử dụng): ").strip()
        if status not in ('0', '1'):
            print("❌ Trạng thái không hợp lệ.")
            return

        new_status = 'free' if status == '0' else 'occupied'
        try:
            parking_slot.update_slot_status(slot_id, new_status)
            print(f"✅ Cập nhật trạng thái chỗ {slot_id} → {new_status}.")
        except Exception as e:
            print(f"❌ Lỗi khi cập nhật trạng thái: {e}")

attendant = ATTENDANT()

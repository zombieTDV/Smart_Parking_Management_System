from config.setting import settings
from src.database import parking_slot, parking_vehicle
from datetime import datetime

class ParkingAttendant:
    def __init__(self):
        # Lấy rate và tổng slot từ cấu hình
        self.rate_per_hour = settings.cfg["parking_slot"]["hourly_rates"]
        self.total_slots   = settings.cfg["parking_slot"]["total_slots"]

        # Đảm bảo các bảng đã được tạo và khởi dữ liệu
        self._ensure_slot_table()
        self._ensure_vehicle_table()

    def _ensure_slot_table(self) -> None:
        """
        Tạo bảng `parking_slot` và chèn các slot theo tổng số.
        """
        parking_slot.create(
            "slot_id INT AUTO_INCREMENT PRIMARY KEY, "
            "available BOOL NOT NULL"
        )
        if parking_slot.count() == 0:
            for _ in range(self.total_slots):
                parking_slot.insert(["available"], (True,))

    def _ensure_vehicle_table(self) -> None:
        """
        Tạo bảng `parking_vehicle` để ghi lịch sử gửi xe.
        """
        parking_vehicle.create(
            "record_id INT AUTO_INCREMENT PRIMARY KEY, "
            "plate_number VARCHAR(20) NOT NULL, "
            "slot_id INT NOT NULL, "
            "check_in DATETIME NOT NULL"
        )

    def view_available_slots(self) -> None:
        """
        In danh sách các slot còn trống.
        """
        rows      = parking_slot.select_all()
        free_ids  = [row[0] for row in rows if row[1]] # type: ignore
        print("Available Slots:", free_ids)

    def check_in_vehicle(self, plate_number: str) -> None:
        """
        Gán slot đầu tiên rảnh cho xe, đánh dấu occupied,
        và lưu bản ghi gửi xe vào table `parking_vehicle`.
        """
        rows = parking_slot.select_all()
        free = [r for r in rows if r[1]] # type: ignore
        if not free:
            print("No available slots right now.")
            return

        slot_id = free[0][0] # type: ignore
        # Cập nhật slot
        parking_slot.update(slot_id, {"available": False})
        # Chèn record xe
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        parking_vehicle.insert(
            ["plate_number", "slot_id", "check_in"],
            (plate_number, slot_id, now)
        )
        print(f"Vehicle {plate_number} checked in at slot {slot_id}.")

    def check_out_vehicle(self, plate_number: str) -> None:
        """
        Tìm record xe, tính phí, giải phóng slot, xóa record.
        """
        # Lấy tất cả bản ghi và tìm xe
        records = parking_vehicle.select_all()
        rec = next(
            (r for r in records if r[1] == plate_number),
            None
        )
        if not rec:
            print("Vehicle not found.")
            return

        record_id, _, slot_id, check_in_str = rec
        check_in = datetime.strptime(check_in_str, "%Y-%m-%d %H:%M:%S")

        # Tính số giờ (làm tròn lên)
        delta   = datetime.now() - check_in
        hours   = int(delta.total_seconds() // 3600)
        if delta.total_seconds() % 3600:
            hours += 1

        fee = hours * self.rate_per_hour

        # Giải phóng slot và xóa bản ghi
        parking_slot.update(slot_id, {"available": True})
        parking_vehicle.delete(record_id)

        print(f"Vehicle {plate_number} checked out from slot {slot_id}.")
        print(f"Hours parked: {hours}, Fee: ${fee}")


# Khởi tạo attendant
attendant = ParkingAttendant()

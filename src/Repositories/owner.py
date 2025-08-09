from src.database import parking_slot
class User:
    def __init__(self):
        pass

    def track_availability(self) -> None:
        select = parking_slot.select_all()
        print("=== Parking Status ===")
        for i in range(parking_slot.count()):
            if select[i][1] == 1:
                print(f"ID: {select[i][0]}  ----- availability: Free")
            else:
                print(f"ID: {select[i][0]}  ----- availability: Occupied")

from config.setting import settings
from src.database import parking_slot, transaction_repo
from src.models import Transaction

class OWNER:
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
            print(f"- ID: {slot.id} | Vị trí: {slot.location or 'N/A'}")

    def pay_parking_fee(self):
        """
        Cho phép chủ xe kiểm tra phí và thanh toán giao dịch đang mở.
        """
        plate = input("Nhập biển số xe: ").strip().upper()
        tr = transaction_repo.get_active_transaction_by_plate(plate)
        if not tr:
            print("❌ Không có giao dịch đang chờ thanh toán.")
            return

        hours = tr.calculate_duration_hours()
        fee   = hours * settings.hourly_rate
        print(f"\nThời gian đỗ: {hours} giờ")
        print(f"Phí phải thanh toán: {fee} VND")

        confirm = input("Thanh toán ngay? (y/n): ").strip().lower()
        if confirm == 'y':
            transaction_repo.close_transaction(tr.id, fee)
            parking_slot.release_slot(tr.slot_id)
            print("✅ Thanh toán thành công. Cảm ơn bạn đã sử dụng dịch vụ.")
        else:
            print("❌ Thanh toán đã hủy.")

owner = OWNER()
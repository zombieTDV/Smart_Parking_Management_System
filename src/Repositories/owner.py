from config.setting import settings
from src.models.parking_slot import parking_slot#, transaction_repo
# from src.models import Transaction

class CarOwner:
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
            print(f"- ID: {slot[0]}") # type: ignore

    # def pay_parking_fee(self):
    #     """
    #     Cho phép chủ xe kiểm tra phí và thanh toán giao dịch đang mở.
    #     """
    #     tr = transaction_repo.pay()
    #     if not tr:
    #         print("❌ Không có giao dịch đang chờ thanh toán.")
    #         return

    #     hours = tr.calculate_duration_hours()
    #     fee = hours * settings.hourly_rates
    #     print(f"\nThời gian đỗ: {hours} giờ")
    #     print(f"Phí phải thanh toán: {fee} VND")

    #     confirm = input("Thanh toán ngay? (y/n): ").strip().lower()
    #     if confirm == 'y':
    #         transaction_repo.close_transaction(tr.id, fee)
    #         parking_slot.release_slot(tr.slot_id)
    #         print("✅ Thanh toán thành công. Cảm ơn bạn đã sử dụng dịch vụ.")
    #     else:
    #         print("❌ Thanh toán đã hủy.")
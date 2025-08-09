from src.database import parking_slot

class ParkingService:
    def view_available_slots(self):
        slots = parking_slot.select_all()
        available = [slot for slot in slots if slot[1] == 1]
        print("Available slots:", [slot[0] for slot in available])
        return available

    def view_occupied_slots(self):
        slots = parking_slot.select_all()
        occupied_info = []
        for slot in slots:
            if slot[1] == 0:
                plate = parking_slot.get_plate_by_slot(slot[0])
                print(f"Chỗ {slot[0]} có xe biển số {plate}.")
                occupied_info.append((slot[0], plate))
        return occupied_info if occupied_info else "Không có xe nào đang đỗ."

    def check_in_vehicle(self, plate_number):
        slots = self.view_available_slots()
        if not slots:
            print("No available slots.")
            return None
        slot_id = slots[0][0]
        parking_slot.assign_vehicle(slot_id, plate_number)
        print(f"Vehicle {plate_number} checked in at slot {slot_id}.")
        return slot_id

    def check_out_vehicle(self, plate_number):
        slot_id = parking_slot.release_vehicle(plate_number)
        if slot_id:
            print(f"Vehicle {plate_number} checked out from slot {slot_id}.")
        else:
            print("Vehicle not found.")
        return slot_id
    

    
    
class ParkingService:
    # ...existing code...

    def add_parking_slot(self, slot_id):
        parking_slot.add_slot(slot_id)
        print(f"Đã thêm chỗ đỗ xe mới: {slot_id}")

    def remove_parking_slot(self, slot_id):
        parking_slot.remove_slot(slot_id)
        print(f"Đã xóa chỗ đỗ xe: {slot_id}")

    def update_slot_status(self, slot_id, is_available):
        parking_slot.update_status(slot_id, is_available)
        status = "Free" if is_available else "Occupied"
        print(f"Chỗ {slot_id} đã được cập nhật trạng thái: {status}")

    def calculate_fee(self, plate_number, rate_per_hour=5):
        check_in, check_out = parking_slot.get_times(plate_number)
        if not check_in or not check_out:
            print("Không tìm thấy thông tin thời gian gửi xe.")
            return None
        duration = (check_out - check_in).total_seconds() / 3600
        fee = int(duration) * rate_per_hour
        print(f"Phí gửi xe cho {plate_number}: {fee} VND")
        return fee
    
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
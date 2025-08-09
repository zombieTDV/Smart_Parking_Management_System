from src.database import parking_slot
from src.controllers.admin_controller import admin
from src.controllers.owner_controller import User


if __name__ == "__main__":
    John = User()
    # parking_slot.init_parking_slots(size = 10)
    # # database_management.clear_table("parking_slot")

    # print(f"Number of rows: {parking_slot.count()}") 
    
    
    # admin.track_availability()

    John.track_availability()
    
    print("Exit!")

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

    def check_available_slots(self) -> None:
        select = parking_slot.select_all()
        print("=== Available Parking Slots ===")
        for i in range(parking_slot.count()):
            if select[i][1] == 1:
                print(f"ID: {select[i][0]} is Free")

    
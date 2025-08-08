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
    
    
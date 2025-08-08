from src.database import parking_slot
from config.setting import settings
from src.controllers.admin_controller import admin


if __name__ == "__main__":
    # parking_slot.init_parking_slots(size = 10)
    # database_management.clear_table("parking_slot")

    print(f"Number of rows: {parking_slot.count()}") 
    
    
    admin.track_availability()
    
    print("Exit!")
    # admin.track_availability()
    
    
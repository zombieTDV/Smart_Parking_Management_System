from src.database import parking_slot
from src.controllers.admin_controller import admin


if __name__ == "__main__":
    print(f"Number of rows: {parking_slot.count()}") 
    
    
    admin.track_availability()
    
    print("Exit!")
    
    
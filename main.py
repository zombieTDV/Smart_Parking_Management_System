from src.database import parking_slot
from src.Repositories.admin import admin
from src.Repositories.owner import User
from src.cli.menu import show_main_menu

if __name__ == "__main__":
    show_main_menu()
    
    # John = User()
    # parking_slot.init_parking_slots(size = 10)
    # # database_management.clear_table("parking_slot")

    # print(f"Number of rows: {parking_slot.count()}") 
    
    
    # admin.track_availability()

    # John.track_availability()
    
    print("Exit!")
    
    
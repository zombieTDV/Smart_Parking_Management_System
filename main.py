from src.database import parking_slot
from src.Repositories.admin import admin
from src.Repositories.owner import User
from src.cli.menu import show_main_menu

if __name__ == "__main__":
    admin.set_up_parking_slots(10)  # Set up parking slots with a size of 10

    # Uncomment to configure parking lot settings
    # admin.configure_parking_lot()
    
    
    admin.manage_parking_slots()

    # John.track_availability()
    
    print("Exit!")
    
    
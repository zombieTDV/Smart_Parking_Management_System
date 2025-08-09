from src.cli.menu import attendant_menu, owner_menu
from src.database import parking_slot
from src.Repositories.admin import admin
 class User:
    def __init__(selt):
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

admin= user()                       

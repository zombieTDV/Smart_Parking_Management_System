from config.setting import settings
from src.database import parking_slot
class ADMIN():
    def __init__(self) -> None:
        pass 
    
    #Configure parking lot settings 
    def set_total_slots(self, total_slots: int) -> None:        
        settings.cfg["parking_slot"]["total_slots"]= total_slots
        settings.save()
        
    def set_hourly_rates(self, hourly_rates: float) -> None:
        settings.cfg["parking_slot"]["hourly_rates"]= hourly_rates
        settings.save()
    
    
    def track_availability(self) -> None:
        select = parking_slot.select_all()
        print("=== Parking Status ===")
        for i in range(parking_slot.count()):
            if select[i][1] == 1: # type: ignore
                print(f"ID: {select[i][0]}  ----- availability: Free") # type: ignore
            else:
                print(f"ID: {select[i][0]}  ----- availability: Occupied") # type: ignore
    
    

admin = ADMIN()
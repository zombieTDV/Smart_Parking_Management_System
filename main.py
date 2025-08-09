from src.Repositories.admin import admin
from src.models.acount import Acount

# from src.Repositories.attendant import ParkingAttendant
# from src.Repositories.owner import User
from src.cli.menu import show_main_menu

if __name__ == "__main__":
    admin.delete_all_accounts()
    
    new_user = Acount(username = "VuongUTH", role = "admin", password= "123456789")
    new_user.save_to_db()
    # new_user.display_acount()
    
    admin.view_all_accounts()
    # show_main_menu()
    
    
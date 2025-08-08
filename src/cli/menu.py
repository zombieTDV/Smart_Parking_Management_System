
from src.cli.menu import show_main_menu

if __name__ == "__main__":
    show_main_menu()
from src.controllers.admin_controller import admin_menu
from src.controllers.attendant_controller import attendant_menu
from src.controllers.owner_controller import owner_menu

def show_main_menu():
    while True:
        print("\n====== SMART PARKING SYSTEM ======")
        print("1. Đăng nhập Admin")
        print("2. Đăng nhập Nhân viên giữ xe")
        print("3. Đăng nhập Chủ xe")
        print("0. Thoát")

        choice = input("Chọn vai trò: ")

        if choice == '1':
            admin_menu()
        elif choice == '2':
            attendant_menu()
        elif choice == '3':
            owner_menu()
        elif choice == '0':
            print("Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ.")

def admin_menu():
    pass

def attendant_menu():
    pass

def owner_menu():
    pass


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



from src.cli.menu import show_main_menu

if __name__ == "__main__":
    show_main_menu()


from src.Repositories import admin, attendant, owner

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

def admin_menu():
    while True:
        print("\n--- Menu Admin ---")
        print("1. Cấu hình bãi đỗ")
        print("2. Quản lý chỗ đỗ")
        print("3. Xem báo cáo doanh thu")
        print("0. Quay lại")

        choice = input("Chọn: ")

        if choice == '1':
            admin.configure_parking_lot()
        elif choice == '2':
            admin.manage_parking_slots()
        elif choice == '3':
            admin.generate_revenue_report()
        elif choice == '0':
            break
        else:
            print("Lựa chọn không hợp lệ.")

def attendant_menu():
    while True:
        print("\n--- Menu Nhân viên giữ xe ---")
        print("1. Check-in xe")
        print("2. Check-out xe")
        print("3. Cập nhật trạng thái chỗ đỗ")
        print("0. Quay lại")

        choice = input("Chọn: ")

        if choice == '1':
            attendant.check_in_vehicle()
        elif choice == '2':
            attendant.check_out_vehicle()
        elif choice == '3':
            attendant.update_slot_status()
        elif choice == '0':
            break
        else:
            print("Lựa chọn không hợp lệ.")

def owner_menu():
    while True:
        print("\n--- Menu Chủ xe ---")
        print("1. Xem chỗ đỗ còn trống")
        print("2. Xem và thanh toán phí")
        print("0. Quay lại")

        choice = input("Chọn: ")

        if choice == '1':
            owner.view_available_slots()
        elif choice == '2':
            owner.pay_parking_fee()
        elif choice == '0':
            break
        else:
            print("Lựa chọn không hợp lệ.")


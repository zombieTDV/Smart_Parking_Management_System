# src/cli/menu.py

from src.Repositories.admin import admin
from src.Repositories.owner import CarOwner
import src.Repositories.attendant as attendant
from src.models.parking_slot import parking_slot
import src.services.auth_service as auth
from src.services.parking_service import calculate_fee, view_available_slots, check_in_vehicle, check_out_vehicle, find_slot_id_by_user_id, find_user_id_by_username
from src.models.transaction import transaction_service
from src.models.account import accounts_central

car_owner = None

def show_main_menu():
    while True:
        print("\n====== SMART PARKING SYSTEM ======")
        print("1. Đăng nhập Admin")
        print("2. Đăng nhập Nhân viên giữ xe")
        print("3. Đăng nhập Chủ xe")
        print("\n")
        print("======== Đăng ký =======")
        print("4. Đăng ký Admin mới")
        print("5. Đăng ký Nhân viên giữ xe mới")
        print("6. Đăng ký Chủ xe mới (Car Owner)")
        print("\n")
        print("======== Thoát ========")
        print("0. Thoát")

        choice = input("Chọn dịch vụ: ").strip()

        if choice == '1':
            if auth.login_admin():
                admin_menu()
        elif choice == '2':
            if auth.login_attendant():
                attendant_menu()
        elif choice == '3':
            print("\n--- Đăng nhập Chủ xe ---")
            username = input("Tên đăng nhập: ").strip()
            password = input("Mật khẩu: ").strip()
            if auth.login_car_owner(username, password):
                car_owner_menu(username, password)
            
        elif choice == '4':
            auth.resiger_admin()
        elif choice == '5':
            auth.register_attendant()
        elif choice == '6':
            auth.register_car_owner()
        elif choice == '0':
            print("Cảm ơn bạn đã sử dụng hệ thống. Tạm biệt!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ.")



def admin_menu():
    while True:
        print("\n--- Menu Admin ---")
        print("1. Cập nhật tổng số chỗ đỗ")
        print("2. Cập nhật giá theo giờ")
        print("===== Quản lý ===")
        print("3. Tình trạng các chỗ đỗ")
        print("4. Xem lịch sử giao dịch")
        print("===== Quản lý cơ sở dữ liệu ===")
        print("5. Quản lý cơ sở dữ liệu")
        print("0. Quay lại")

        choice = input("Chọn: ").strip()
        if choice == '1':
            admin.set_total_slots(int(input(f"Tổng số chỗ cũ: {parking_slot.total_slots}\nNhập tổng số chỗ đỗ mới: ")))
        elif choice == '2':
            admin.set_hourly_rates(float(input(f"Giá theo giờ cũ: {parking_slot.hourly_rates}\nNhập giá theo giờ mới: ")))
        elif choice == '3':
            admin.view_available_slots()
        elif choice == '4':
            transaction_service.view_all_records()
            
        elif choice == '5':
            print("\n--- Quản lý cơ sở dữ liệu ---")
            print("1. Quản lý chỗ đỗ")
            print("2. Quản lý tài khoản")
            print("3. Quản lý giao dịch")
            print("0. Quay lại")
            db_choice = input("Chọn: ").strip()
            if db_choice == '1':
                print("\n--- Quản lý chỗ đỗ ---")
                print("1. Xem tất cả chỗ đỗ")
                print("2. Giải phóng chỗ đỗ")
                print("3. Xóa tất cả chỗ đỗ")
                print("4. Xóa bảng chỗ đỗ")
                db_slot_choice = input("Chọn: ").strip()
                if db_slot_choice == '1':
                    parking_slot.view_available_slots()
                elif db_slot_choice == '2':
                    slot_id = int(input("Nhập ID chỗ đỗ cần giải phóng: "))
                    parking_slot.release_slot(slot_id)
                elif db_slot_choice == '3':
                    parking_slot.delete_all_slots()
                    print("✅ Đã xóa tất cả chỗ đỗ.")
                elif db_slot_choice == '4':
                    parking_slot.table.drop()
                    print("✅ Đã xóa bảng chỗ đỗ.")
                else:
                    print("❌ Lựa chọn không hợp lệ.")
            elif db_choice == '2':
                print("\n--- Quản lý tài khoản ---")
                print("1. Xem tất cả tài khoản")
                print("2. Xóa tài khoản theo ID")
                print("3. Xóa tất cả tài khoản")
                print("4. Xóa bảng tài khoản")
                db_account_choice = input("Chọn: ").strip()
                if db_account_choice == '1':
                    accounts_central.view_all_accounts()
                elif db_account_choice == '2':
                    account_id = int(input("Nhập ID tài khoản cần xóa: "))
                    accounts_central.delete_account(account_id)
                elif db_account_choice == '3':
                    accounts_central.delete_all_accounts()
                    print("✅ Đã xóa tất cả tài khoản.")
                elif db_account_choice == '4':
                    accounts_central.table.drop()
                    print("✅ Đã xóa bảng tài khoản.")
                else:
                    print("❌ Lựa chọn không hợp lệ.")
            elif db_choice == '3':
                print("\n--- Quản lý giao dịch ---")
                print("1. Xem tất cả giao dịch")
                print("2. Xóa giao dịch theo ID")
                print("3. Xóa tất cả giao dịch")
                print("4. Xóa bảng giao dịch")
                db_transaction_choice = input("Chọn: ").strip()
                if db_transaction_choice == '1':
                    transaction_service.view_all_records()
                elif db_transaction_choice == '2':
                    ID = int(input("Nhập ID người dùng: "))
                    id_slot = int(input("Nhập ID chỗ đỗ: "))
                    transaction_service.delete_record(ID, id_slot)
                elif db_transaction_choice == '3':
                    transaction_service.delete_all_records()
                    print("✅ Đã xóa tất cả giao dịch.")
                elif db_transaction_choice == '4':  
                    transaction_service.table.drop()
                    print("✅ Đã xóa bảng giao dịch.")
                else:
                    print("❌ Lựa chọn không hợp lệ.")
            elif db_choice == '0':
                continue
            
        elif choice == '0':
            break
        else:
            print("❌ Lựa chọn không hợp lệ.")


def attendant_menu():
    while True:
        print("\n--- Menu Nhân viên giữ xe ---")
        print("1. Check-in xe")
        print("2. Check-out xe")
        print("3. Xem trạng thái chỗ đỗ")
        print("4. Xem lịch sử giao dịch")
        print("0. Quay lại")

        choice = input("Chọn: ").strip()
        if choice == '1':
            check_in_vehicle(username=input("Nhập Username: "), user_id= int(input("Nhập ID người dùng: ")), slot_id= int(input("Nhập ID chỗ đỗ: ")))
        elif choice == '2':
            check_out_vehicle(int(input("Nhập ID người dùng: ")), int(input("Nhập ID chỗ đỗ: ")))
        elif choice == '3':
            view_available_slots()
        elif choice == '4':
            transaction_service.view_all_records()
        elif choice == '0':
            break
        else:
            print("❌ Lựa chọn không hợp lệ.")


def car_owner_menu(username: str, password: str):
    while True:
        print("\n--- Menu Chủ xe ---")
        print("1. Xem thông tin chỗ đỗ")
        print("2. Thanh toán")
        print("0. Quay lại")

        choice = input("Chọn: ").strip()
        if choice == '1':
            parking_slot.view_available_slots()
        elif choice == '2':
            print(f"Số tiền thanh toán: {calculate_fee(find_user_id_by_username(username), find_slot_id_by_user_id(username))} VND")
            
            transaction_service.check_out_vehicle(find_user_id_by_username(username), find_slot_id_by_user_id(username))
        elif choice == '0':
            break
        else:
            print("❌ Lựa chọn không hợp lệ.")

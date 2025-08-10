# src/cli/menu.py

from src.Repositories.admin import admin
from src.Repositories.owner import CarOwner

from src.models.parking_slot import parking_slot
from src.models.transaction import transaction_service
from src.models.account import accounts_central

import src.services.auth_service as auth
from src.services.parking_service import calculate_fee, view_available_slots, check_in_vehicle, check_out_vehicle
from src.services import report_service


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
                car_owner = CarOwner(username, password)
                car_owner_menu(car_owner)
            
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
        print("===== Báo cáo doanh thu ===")
        print("6. In báo cáo doanh thu")
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
                    ID = int(input("Nhập ID giao dịch: "))
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
        elif choice == '6':
            print("\n--- Chọn loại báo cáo ---")
            print("1. Báo cáo theo ngày")
            print("2. Báo cáo theo tháng")
            print("3. Báo cáo theo năm")
            print("0. Quay lại")
            report_choice = input("Chọn: ").strip()
            if report_choice == '1':
                report_service.day_revenue_report()
            elif report_choice == '2':
                report_service.month_revenue_report()
            elif report_choice == '3':
                report_service.year_revenue_report()
            elif report_choice == '0':
                continue
            else:
                print("❌ Lựa chọn không hợp lệ.")
            
            
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
            check_in_vehicle(username=input("Nhập Username: "), slot_id= int(input("Nhập ID chỗ đỗ: ")))
        elif choice == '2':
            check_out_vehicle(int(input("Nhập ID giao dịch: ")), int(input("Nhập ID chỗ đỗ: ")))
        elif choice == '3':
            view_available_slots()
        elif choice == '4':
            transaction_service.view_all_records()
        elif choice == '0':
            break
        else:
            print("❌ Lựa chọn không hợp lệ.")


def car_owner_menu(car_owner: CarOwner):
    parking_slot.view_available_slots()
    ID = int(input("Nhập ID giao dịch: "))
    ID_slot = int(input("Nhập ID chỗ đỗ: "))
    while True:
        car_owner.fee = calculate_fee(ID, ID_slot)
        
        print(f"\n--- Menu Chủ xe ---  || Username:  {car_owner.username}, Payment Status: {transaction_service.get_payment_status(ID)} || {car_owner.fee} VND")
        print("1. Xem thông tin chỗ đỗ")
        print("2. Check in Online")
        print("3. Thanh toán")
        print("0. Quay lại")

        choice = input("Chọn: ").strip()
        if choice == '1':
            parking_slot.view_available_slots()
            
        elif choice == '2':
            slot_id = int(input("Nhập ID chỗ đỗ bạn muốn: "))
            if parking_slot.is_slot_available(slot_id):
                check_in_vehicle(slot_id, car_owner.username)
                print(f"✅ Xe của bạn đã được check-in vào chỗ đỗ ID {slot_id}.")
        elif choice == '3':
            check_out_vehicle(ID, ID_slot)
        elif choice == '0':
            break
        else:
            print("❌ Lựa chọn không hợp lệ.")

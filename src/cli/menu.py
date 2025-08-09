from src.Repositories.admin import admin
from src.models.parking_slot import parking_slot
from config.setting import settings

# menu.py

from src.Repositories.admin import admin
# from src.Repositories.attendant import attendant
# from src.Repositories.owner import owner
# from src.Repositories.auth import auth

# Tài khoản admin cố định
ADMIN_CREDENTIALS = {
    "username": "",
    "password": ""
}

def show_main_menu():
    while True:
        print("\n====== SMART PARKING SYSTEM ======")
        print("1. Đăng nhập Admin")
        print("2. Đăng nhập Nhân viên giữ xe")
        print("3. Đăng nhập Chủ xe")
        print("4. Đăng ký Chủ xe mới")
        print("0. Thoát")

        choice = input("Chọn vai trò: ").strip()

        if choice == '1':
            login_admin()
        elif choice == '2':
            # login_attendant()
            pass
        elif choice == '3':
            pass
            # login_owner()
        elif choice == '4':
            pass
            # register_owner()
        elif choice == '0':
            print("Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ.")

# Hàm xác thực Admin
def login_admin():
    print("\n--- Đăng nhập Admin ---")
    username = input("Tên đăng nhập: ").strip()
    password = input("Mật khẩu: ").strip()

    if username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
        print("✅ Đăng nhập Admin thành công.")
        admin_menu()
    else:
        print("❌ Sai tên đăng nhập hoặc mật khẩu Admin.")

# Hàm xác thực và chuyển vào Menu Nhân viên
# def login_attendant():
#     print("\n--- Đăng nhập Nhân viên giữ xe ---")
#     username = input("Tên đăng nhập: ").strip()
#     password = input("Mật khẩu: ").strip()

#     if auth.validate_attendant(username, password):
#         print(f"✅ Đăng nhập thành công: Nhân viên [{username}]")
#         attendant_menu()
#     else:
#         print("❌ Sai tên đăng nhập hoặc mật khẩu Nhân viên.")

# Hàm xác thực và chuyển vào Menu Chủ xe
# def login_owner():
#     print("\n--- Đăng nhập Chủ xe ---")
#     username = input("Tên đăng nhập: ").strip()
#     password = input("Mật khẩu: ").strip()

#     if auth.validate_owner(username, password):
#         print(f"✅ Đăng nhập thành công: Chủ xe [{username}]")
#         owner_menu()
#     else:
#         print("❌ Sai tên đăng nhập hoặc mật khẩu Chủ xe.")

# # Hàm đăng ký Chủ xe mới
# def register_owner():
#     print("\n--- Đăng ký Chủ xe mới ---")
#     while True:
#         username = input("Chọn tên đăng nhập: ").strip()
#         if auth.owner_exists(username):
#             print("❌ Tên đăng nhập đã tồn tại, vui lòng chọn tên khác.")
#             continue

#         password = input("Chọn mật khẩu: ").strip()
#         confirm  = input("Nhập lại mật khẩu: ").strip()

#         if password != confirm:
#             print("❌ Mật khẩu không khớp, vui lòng thử lại.")
#             continue

#         auth.register_owner(username, password)
#         print(f"✅ Đăng ký thành công Chủ xe [{username}]. Vui lòng đăng nhập để sử dụng.")
#         break

def admin_menu():
    while True:
        print("\n--- Menu Admin ---")
        print("1. Cập nhật tổng số chỗ đỗ")
        print("2. Cập nhật giá theo giờ")
        print("3. Tình trạng các chỗ đỗ")
        print("0. Quay lại")

        choice = input("Chọn: ").strip()

        if choice == '1':
            admin.set_total_slots(int(input(f"Tổng số chỗ cũ: {parking_slot.total_slots}\n\tNhập tổng số chỗ đỗ mới: ")))
        elif choice == '2':
            admin.set_hourly_rates(float(input(f"Giá theo giờ cũ: {parking_slot.hourly_rates}\n\tNhập giá theo giờ mới: ")))
        elif choice == '3':
            admin.view_available_slots()
        elif choice == '0':
            break
        else:
            print("Lựa chọn không hợp lệ.")

# Hàm tạo tài khoản Nhân viên giữ xe do Admin gọi
# def create_attendant_account():
#     print("\n--- Tạo tài khoản Nhân viên giữ xe ---")
#     while True:
#         username = input("Chọn tên đăng nhập: ").strip()
#         if auth.attendant_exists(username):
#             print("❌ Tên đăng nhập đã tồn tại, vui lòng chọn tên khác.")
#             continue

#         password = input("Chọn mật khẩu: ").strip()
#         confirm  = input("Nhập lại mật khẩu: ").strip()

#         if password != confirm:
#             print("❌ Mật khẩu không khớp, vui lòng thử lại.")
#             continue

#         auth.register_attendant(username, password)
#         print(f"✅ Tạo tài khoản Nhân viên giữ xe [{username}] thành công.")
#         break

# def attendant_menu():
#     while True:
#         print("\n--- Menu Nhân viên giữ xe ---")
#         print("1. Check-in xe")
#         print("2. Check-out xe")
#         print("3. Cập nhật trạng thái chỗ đỗ")
#         print("0. Quay lại")

#         choice = input("Chọn: ").strip()

#         # if choice == '1':
#         #     attendant.check_in_vehicle()
#         # elif choice == '2':
#         #     attendant.check_out_vehicle()
#         # elif choice == '3':
#         #     attendant.update_slot_status()
#         # elif choice == '0':
#         #     break
#         # else:
#         #     print("Lựa chọn không hợp lệ.")

# def owner_menu():
#     while True:
#         print("\n--- Menu Chủ xe ---")
#         print("1. Xem chỗ đỗ còn trống")
#         print("2. Xem và thanh toán phí")
#         print("0. Quay lại")

#         choice = input("Chọn: ").strip()

#         if choice == '1':
#             owner.view_available_slots()
#         elif choice == '2':
#             owner.pay_parking_fee()
#         elif choice == '0':
#             break
#         else:
#             print("Lựa chọn không hợp lệ.")
        
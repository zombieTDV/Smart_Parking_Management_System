from src.models.account import Account, accounts_central
# ----- Register -----
def resiger_admin():
    admin = Account()
    
    print("\n--- Đăng ký Admin mới ---")
    
    admin.create_account()
    admin.save_to_db()
    
    print("✅ Đăng ký Admin thành công.")
    print(f"Tài khoản: {admin.username}, Vai trò: {admin.role}")
    print("Vui lòng đăng nhập lại với tài khoản mới.")

def register_attendant():
    attendant = Account()
    
    print("\n--- Đăng ký Nhân viên mới (Attendant) ---")
    attendant.create_account()
    attendant.save_to_db()
    
    print("✅ Đăng ký Nhân viên thành công.")
    print(f"Tài khoản: {attendant.username}, Vai trò: {attendant.role}")

def register_car_owner():
    owner = Account()
    
    print("\n--- Đăng ký Chủ xe mới (Car Owner) ---")
    owner.create_account()
    owner.save_to_db()
    
    print("✅ Đăng ký Chủ xe thành công.")
    print(f"Tài khoản: {owner.username}, Vai trò: {owner.role}")
    
    
#--- Login -----
def login_admin() ->bool:
    print("\n--- Đăng nhập Admin ---")
    username = input("Tên đăng nhập: ").strip()
    password = input("Mật khẩu: ").strip()

    if validate_admin(username, password):
        print(f"✅ Đăng nhập thành công: Admin [{username}]")
        return True
    else:
        print("❌ Sai tên đăng nhập hoặc mật khẩu Admin.")
        return False


def login_attendant() ->bool:
    print("\n--- Đăng nhập Nhân viên giữ xe ---")
    username = input("Tên đăng nhập: ").strip()
    password = input("Mật khẩu: ").strip()
    
    if validate_attendant(username, password):
        print(f"✅ Đăng nhập thành công: Nhân viên [{username}]")
        return True
    else:
        print("❌ Sai tên đăng nhập hoặc mật khẩu Nhân viên.")
        return False


def login_car_owner(username: str, password: str) ->bool:
    if validate_car_owner(username, password):
        print(f"✅ Đăng nhập thành công: Chủ xe [{username}]")
        return True
    else:
        print("❌ Sai tên đăng nhập hoặc mật khẩu Chủ xe.")
        return False


# ----- Validation -----
def validate_admin(username: str, password: str) -> bool:
    """
    Kiểm tra xem tài khoản Admin có hợp lệ hay không.
    """
    try:
        admin_account = accounts_central.find_record_with_value(column='username', value=username)[0] # type: ignore
        if admin_account[2] == 'admin' and admin_account[3] == password:  # type: ignore
            return True
    except:
        return False
    
    return False

def validate_attendant(username: str, password: str) -> bool:
    """
    Kiểm tra xem tài khoản Attendant có hợp lệ hay không.
    """
    try:
        record = accounts_central.find_record_with_value(column='username', value=username)[0]  # type: ignore
        if record[2] == 'attendant' and record[3] == password: # type: ignore
            return True
    except:
        return False
    return False

def validate_car_owner(username: str, password: str) -> bool:
    """
    Kiểm tra xem tài khoản Car Owner có hợp lệ hay không.
    """
    try:
        record = accounts_central.find_record_with_value(column='username', value=username)[0]  # type: ignore
        if record[2] == 'owner' and record[3] == password:  # type: ignore # role & password
            return True
    except:
        return False
    return False




